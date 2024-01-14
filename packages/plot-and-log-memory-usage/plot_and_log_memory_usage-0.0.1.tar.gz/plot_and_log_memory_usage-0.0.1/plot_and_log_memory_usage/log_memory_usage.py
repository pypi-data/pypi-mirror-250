import tyro
from dataclasses import dataclass
from datetime import datetime
import pathlib
import os
from plot_and_log_memory_usage.utils import (
    get_cpu_memory_usage,
    get_gpu_memory_usage,
    get_num_gpus,
    datetime_to_str,
)
import time


@dataclass
class Args:
    log_period_sec: float = 5.0
    log_folderpath: pathlib.Path = (
        pathlib.Path("~").expanduser() / "logged_memory_usage"
    )
    print_updates: bool = True


def main() -> None:
    args: Args = tyro.cli(Args)

    args.log_folderpath.mkdir(parents=True, exist_ok=True)

    log_filepath = args.log_folderpath / f"{datetime_to_str(datetime.now())}.csv"
    num_gpus = get_num_gpus()

    if args.print_updates:
        print(f"Logging to {log_filepath}")

    with open(log_filepath, "a") as log_file:
        # Write header
        log_file.write("DateTime,CPU_Used_MB,CPU_Total_MB")
        for i in range(num_gpus):
            log_file.write(f",GPU_{i}_Used_MB,GPU_{i}_Total_MB")
        log_file.write("\n")

        while True:
            log_line_list = []
            cpu_usage = get_cpu_memory_usage()
            datetime_str = datetime_to_str(datetime.now())
            log_line_list.append(
                f"{datetime_str},{cpu_usage.used_mb},{cpu_usage.total_mb}"
            )

            for i in range(num_gpus):
                gpu_usage = get_gpu_memory_usage(i)
                log_line_list.append(f",{gpu_usage.used_mb},{gpu_usage.total_mb}")

            log_line = "".join(log_line_list)
            log_file.write(log_line)
            log_file.write("\n")
            log_file.flush()
            os.fsync(log_file.fileno())

            if args.print_updates:
                print(log_line)

            time.sleep(args.log_period_sec)


if __name__ == "__main__":
    main()
