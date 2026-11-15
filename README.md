# Python DevOps Log Monitoring Tool

A command-line Python utility that scans application logs, counts `ERROR`,
`WARNING`, and `INFO` entries, writes a timestamped report, and returns a
non-zero exit code when the configured error threshold is exceeded.

## Requirements

- Python 3.8+
- No third-party dependencies

## Run on Ubuntu

```bash
python3 --version
python3 monitor.py
```

The default input is `logs/application.log`; the default report is
`reports/monitoring_report.txt`.

## Custom paths and threshold

```bash
python3 monitor.py --log-file logs/application.log \
  --report-file reports/daily_report.txt --error-threshold 1
```

Exit codes:
- `0`: analysis completed and error count is within threshold
- `1`: error count exceeded threshold
- `2`: invalid input, missing log, or file processing error

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Example Git workflow

```bash
git init
git add .
git commit -m "Initial Python DevOps log monitor"
```

Create an empty GitHub repository, then connect it:

```bash
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/python-devops-log-monitor.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Project concepts

- File handling with `pathlib`
- Functions and dictionaries / `Counter`
- Loops and conditional statements
- Exception handling
- Command-line arguments with `argparse`
- Exit codes for automation and CI/CD
- Unit testing with `unittest`
- Git version control
