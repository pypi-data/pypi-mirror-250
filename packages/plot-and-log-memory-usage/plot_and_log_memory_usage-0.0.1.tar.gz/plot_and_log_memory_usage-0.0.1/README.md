# plot_and_log_memory_usage

Scripts for logging CPU and GPU memory usage and subsequently plotting for analysis and debugging

# Installing

Install:

```
pip install plot_and_log_memory_usage
```

# Usage

## Log Memory Usage

Logs memory usage to a file at a given frequency and filepath

```
log_memory_usage --help

usage: log_memory_usage [-h] [--log-period-sec FLOAT] [--log-folderpath PATH] [--print-updates | --no-print-updates]

╭─ arguments ───────────────────────────────────────────────────────────╮
│ -h, --help              show this help message and exit               │
│ --log-period-sec FLOAT  (default: 5.0)                                │
│ --log-folderpath PATH   (default: /home/tylerlum/logged_memory_usage) │
│ --print-updates, --no-print-updates                                   │
│                         (default: True)                               │
╰───────────────────────────────────────────────────────────────────────╯
```

Example:
```
log_memory_usage

Logging to /home/tylerlum/logged_memory_usage/2024-01-13_02-24-22-299722.csv
2024-01-13_02-24-22-324923,7241.94140625,31747.50390625,784.0,4096.0
2024-01-13_02-24-27-381178,7046.80078125,31747.50390625,765.0,4096.0
2024-01-13_02-24-32-504417,7045.4765625,31747.50390625,765.0,4096.0
...
```

## Plot Logged Memory Usage

Creates a plot of the memory usage from the log file for a given timerange

```
plot_logged_memory_usage --help

usage: plot_logged_memory_usage [-h] [OPTIONS]

╭─ options ─────────────────────────────────────────────────────────────╮
│ -h, --help              show this help message and exit               │
│ --end-datetime-str STR  (default: 2024-01-13_02-49-51-581943)         │
│ --start-datetime-str {None}|STR                                       │
│                         (default: None)                               │
│ --lookback-seconds {None}|FLOAT                                       │
│                         (default: None)                               │
│ --log-folderpath PATH   (default: /home/tylerlum/logged_memory_usage) │
│ --save-filepath {None}|PATH                                           │
│                         (default: None)                               │
╰───────────────────────────────────────────────────────────────────────╯
```

You must specify either a start datetime (in the above format) OR lookback seconds (seconds before end datetime)

Example:

```
plot_logged_memory_usage --lookback-seconds 60
```

![plot_logged_memory_usage](https://github.com/tylerlum/plot_and_log_memory_usage/assets/26510814/e451e88e-493e-4009-aeca-706f0a0fa7fd)

```
plot_logged_memory_usage --start-datetime-str "2024-01-13_02-21-50-512677" --save-filepath "output.png"

Saving plot to output.png
```