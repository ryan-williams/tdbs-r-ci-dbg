from .base import cli
from .fetch_runs import fetch_runs
from .download_failure_logs import download_failure_logs
from .extract_errors import extract_errors
from .normalize_errors import normalize_errors
from .summarize import summarize


if __name__ == "__main__":
    cli()
