import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent

URLS_FILE = BASE_DIR / "urls.json"
API_DATA_FILE = BASE_DIR / "api_data.json"
DOWNTIME_LOG = BASE_DIR / "downtime.log"

DEFAULT_TIMEOUT = 5
MAX_RETRIES = 3
MONITOR_INTERVAL = 60


# ---------------------------------------------------------
# Environment Variables
# ---------------------------------------------------------

load_dotenv(BASE_DIR / ".env")

API_TOKEN = os.getenv("API_TOKEN")


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    filename=DOWNTIME_LOG,
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ---------------------------------------------------------
# Load URLs
# ---------------------------------------------------------

def load_urls(file_path):
    """
    Load URLs from urls.json.
    """

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            urls = json.load(file)

        if not isinstance(urls, list):
            raise ValueError("urls.json must contain a list of URLs.")

        return urls

    except FileNotFoundError:
        print(f"URL file not found: {file_path}")
        return []

    except json.JSONDecodeError:
        print("Invalid JSON format in urls.json.")
        return []

    except Exception as error:
        print(f"Error loading URLs: {error}")
        return []


# ---------------------------------------------------------
# HTTP Headers
# ---------------------------------------------------------

def get_headers():
    """
    Build HTTP headers.

    API_TOKEN is optional. It is loaded from the environment
    instead of being hardcoded in the source code.
    """

    headers = {
        "Accept": "application/json",
        "User-Agent": "Python-API-Monitor/1.0"
    }

    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    return headers


# ---------------------------------------------------------
# Check One URL
# ---------------------------------------------------------

def check_url(
    url,
    timeout=DEFAULT_TIMEOUT,
    max_retries=MAX_RETRIES
):
    """
    Check one URL with retry support.

    Returns a dictionary containing:
    - URL
    - status code
    - response time
    - success/failure
    - error message
    """

    headers = get_headers()

    last_error = None

    for attempt in range(1, max_retries + 1):

        start_time = time.perf_counter()

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=timeout
            )

            response_time = round(
                time.perf_counter() - start_time,
                4
            )

            status_code = response.status_code

            result = {
                "url": url,
                "status_code": status_code,
                "response_time_seconds": response_time,
                "success": 200 <= status_code < 400,
                "error": None,
                "checked_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

            # HTTP failure
            if not result["success"]:

                result["error"] = (
                    f"HTTP {status_code}"
                )

                last_error = result["error"]

                if attempt < max_retries:
                    time.sleep(1)
                    continue

                logging.error(
                    "%s | %s",
                    url,
                    result["error"]
                )

            return result

        except requests.exceptions.Timeout:

            response_time = round(
                time.perf_counter() - start_time,
                4
            )

            last_error = "Request timed out"

            if attempt < max_retries:
                time.sleep(1)
                continue

            logging.error(
                "%s | Request timed out",
                url
            )

            return {
                "url": url,
                "status_code": None,
                "response_time_seconds": response_time,
                "success": False,
                "error": last_error,
                "checked_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

        except requests.exceptions.RequestException as error:

            response_time = round(
                time.perf_counter() - start_time,
                4
            )

            last_error = str(error)

            if attempt < max_retries:
                time.sleep(1)
                continue

            logging.error(
                "%s | %s",
                url,
                last_error
            )

            return {
                "url": url,
                "status_code": None,
                "response_time_seconds": response_time,
                "success": False,
                "error": last_error,
                "checked_at": datetime.now().isoformat(
                    timespec="seconds"
                )
            }

    return {
        "url": url,
        "status_code": None,
        "response_time_seconds": None,
        "success": False,
        "error": last_error,
        "checked_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }


# ---------------------------------------------------------
# Save API Data
# ---------------------------------------------------------

def save_api_data(results, file_path):
    """
    Save monitoring results to JSON.
    """

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


# ---------------------------------------------------------
# Display Results
# ---------------------------------------------------------

def display_results(results):

    print("\n" + "=" * 70)
    print("API MONITOR REPORT")
    print("=" * 70)

    for result in results:

        status = (
            "UP"
            if result["success"]
            else "DOWN"
        )

        print(
            f"\nStatus        : {status}"
        )

        print(
            f"URL           : {result['url']}"
        )

        print(
            f"HTTP Status   : {result['status_code']}"
        )

        print(
            f"Response Time : "
            f"{result['response_time_seconds']} seconds"
        )

        if result["error"]:
            print(
                f"Error         : {result['error']}"
            )

    successful = sum(
        1 for result in results
        if result["success"]
    )

    failed = len(results) - successful

    print("\n" + "-" * 70)

    print(f"Total URLs : {len(results)}")
    print(f"Successful : {successful}")
    print(f"Failed     : {failed}")

    print("-" * 70)


# ---------------------------------------------------------
# Monitor Once
# ---------------------------------------------------------

def monitor_once():

    urls = load_urls(URLS_FILE)

    if not urls:
        print("No URLs found to monitor.")
        return []

    results = []

    for url in urls:

        result = check_url(url)

        results.append(result)

    save_api_data(
        results,
        API_DATA_FILE
    )

    display_results(results)

    return results


# ---------------------------------------------------------
# Continuous Monitoring
# ---------------------------------------------------------

def monitor_continuously(
    duration_minutes=10
):
    """
    Monitor URLs every 60 seconds.

    Default duration:
    10 minutes.
    """

    end_time = time.time() + (
        duration_minutes * 60
    )

    run_number = 1

    while time.time() < end_time:

        print(
            f"\nMonitoring run #{run_number}"
        )

        print(
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        monitor_once()

        run_number += 1

        remaining_time = (
            end_time - time.time()
        )

        if remaining_time <= 0:
            break

        sleep_time = min(
            MONITOR_INTERVAL,
            remaining_time
        )

        print(
            f"\nNext check in "
            f"{int(sleep_time)} seconds..."
        )

        time.sleep(sleep_time)

    print("\n10-minute monitoring completed.")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Starting API Monitor...")

    # For initial testing, perform one check.
    monitor_once()

    print("\nInitial API check completed.")


# ---------------------------------------------------------
# Program Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()