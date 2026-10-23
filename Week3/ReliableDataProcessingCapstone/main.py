import argparse
import logging
import os
import sys
from dotenv import load_dotenv
from api_client import ApiClient, ApiClientError
from processor import process_records
from report_generator import write_report

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(),
                    format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = logging.getLogger(__name__)

def run(url, endpoint, output, timeout, retries):
    try:
        payload = ApiClient(url, timeout, retries).get_json(endpoint)
    except (ApiClientError, ValueError) as exc:
        log.error("Retrieval failed; report not updated: %s", exc)
        return 1
    try:
        valid, rejected = process_records(payload)
        path = write_report(valid, rejected, output)
    except (ValueError, OSError, TypeError) as exc:
        log.exception("Processing/report generation failed: %s", exc)
        return 2
    log.info("Complete received=%d processed=%d rejected=%d output=%s",
             len(valid) + len(rejected), len(valid), len(rejected), path)
    print(f"Report written: {path}")
    print(f"Processed: {len(valid)} | Rejected: {len(rejected)}")
    return 0

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Reliable API data processor")
    parser.add_argument("--url", default=os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com"))
    parser.add_argument("--endpoint", default=os.getenv("API_ENDPOINT", "/users"))
    parser.add_argument("--output", default=os.getenv("OUTPUT_PATH", "output/report.json"))
    parser.add_argument("--timeout", type=float, default=float(os.getenv("API_TIMEOUT", "5")))
    parser.add_argument("--retries", type=int, default=int(os.getenv("API_RETRIES", "2")))
    args = parser.parse_args()
    return run(args.url, args.endpoint, args.output, args.timeout, args.retries)

if __name__ == "__main__":
    sys.exit(main())
