import tyro
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List
import pathlib
from plot_and_log_memory_usage.utils import (
    datetime_to_str,
    str_to_datetime,
    str_is_datetime,
    DATETIME_FORMAT,
)
import bisect
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Args:
    end_datetime_str: str = datetime_to_str(datetime.now())
    start_datetime_str: Optional[str] = None
    lookback_seconds: Optional[float] = None
    log_folderpath: pathlib.Path = (
        pathlib.Path("~").expanduser() / "logged_memory_usage"
    )
    save_filepath: Optional[pathlib.Path] = None

    def __post_init__(self) -> None:
        if self.start_datetime_str is None and self.lookback_seconds is None:
            raise ValueError(
                "Either start_datetime_str or lookback_seconds must be specified"
            )
        if self.start_datetime_str is not None and self.lookback_seconds is not None:
            raise ValueError(
                "Only one of start_datetime_str or lookback_seconds may be specified"
            )

    @property
    def start_datetime(self) -> datetime:
        if self.start_datetime_str is not None:
            return str_to_datetime(self.start_datetime_str)
        elif self.lookback_seconds is not None:
            return str_to_datetime(self.end_datetime_str) - timedelta(seconds=self.lookback_seconds)
        raise ValueError("Either start_datetime_str or lookback_seconds must be specified")

    @property
    def end_datetime(self) -> datetime:
        return str_to_datetime(self.end_datetime_str)


def find_valid_datetimes(
    sorted_datetimes: List[datetime], start_datetime: datetime, end_datetime: datetime
) -> List[datetime]:
    # Find the rightmost value less than or equal to start_datetime
    start_idx = bisect.bisect_left(sorted_datetimes, start_datetime)
    if start_idx > 0:
        start_idx -= 1  # Include the log file just before the effective start datetime

    # Find the leftmost value greater than or equal to end_datetime
    end_idx = bisect.bisect_right(sorted_datetimes, end_datetime, lo=start_idx)
    if end_idx == 0:
        raise ValueError(f"No log files found before {end_datetime}")

    # Ensure valid range
    end_idx = min(end_idx, len(sorted_datetimes))

    return sorted_datetimes[start_idx:end_idx]


def filter_and_concatenate_dfs(
    filepaths: List[pathlib.Path], start_datetime: datetime, end_datetime: datetime
) -> pd.DataFrame:
    dfs = []
    for filepath in filepaths:
        df = pd.read_csv(filepath)
        df["DateTime"] = pd.to_datetime(df["DateTime"], format=DATETIME_FORMAT)

        # Filter rows based on the start and end datetime
        filtered_df = df[
            (df["DateTime"] >= start_datetime) & (df["DateTime"] <= end_datetime)
        ]
        dfs.append(filtered_df)

    # Concatenate all filtered dataframes
    concatenated_df = pd.concat(dfs, ignore_index=True)

    # Sort the concatenated dataframe by 'DateTime'
    sorted_df = concatenated_df.sort_values(by="DateTime")
    assert (
        len(sorted_df) > 0
    ), f"No data found between {start_datetime} and {end_datetime}"

    return sorted_df


def main() -> None:
    args: Args = tyro.cli(Args)
    assert (
        args.log_folderpath.exists()
    ), f"Log folderpath {args.log_folderpath} does not exist"

    # Look for log files relevant to the specified datetimes
    filenames = [path.stem for path in args.log_folderpath.iterdir()]
    assert len(filenames) > 0, f"No log files found in {args.log_folderpath}"
    assert all(
        [str_is_datetime(filename) for filename in filenames]
    ), f"Not all filenames in {args.log_folderpath} are valid datetimes: {filenames}"

    sorted_datetimes = sorted([str_to_datetime(filename) for filename in filenames])
    valid_sorted_datetimes = find_valid_datetimes(
        sorted_datetimes=sorted_datetimes,
        start_datetime=args.start_datetime,
        end_datetime=args.end_datetime,
    )

    # Read in the log files and concatenate them
    sorted_df = filter_and_concatenate_dfs(
        filepaths=[
            args.log_folderpath / f"{datetime_to_str(datetime)}.csv"
            for datetime in valid_sorted_datetimes
        ],
        start_datetime=args.start_datetime,
        end_datetime=args.end_datetime,
    )

    # Plot
    cpu_used_columns = [
        col for col in sorted_df.columns if "CPU" in col and "Used" in col
    ]
    gpu_used_columns = [
        col for col in sorted_df.columns if "GPU" in col and "Used" in col
    ]
    used_columns = cpu_used_columns + gpu_used_columns
    total_columns = [col.replace("Used", "Total") for col in used_columns]
    fig, axes = plt.subplots(
        nrows=len(cpu_used_columns) + len(gpu_used_columns), ncols=1, figsize=(10, 8)
    )
    axes = axes.flatten()
    for i, (used_col, total_col) in enumerate(zip(used_columns, total_columns)):
        sorted_df.plot(
            x="DateTime",
            y=used_col,
            ax=axes[i],
            title=used_col,
            ylim=(0, sorted_df[total_col].max()),
        )
        axes[i].grid()

    plt.tight_layout()

    if args.save_filepath:
        print(f"Saving plot to {args.save_filepath}")
        plt.savefig(args.save_filepath)

    plt.show()


if __name__ == "__main__":
    main()
