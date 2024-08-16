from .base import cli
from .fetch_runs import fetch_runs
from .download_failure_logs import download_failure_logs
from .extract_errors import extract_errors


if __name__ == "__main__":
    cli()
