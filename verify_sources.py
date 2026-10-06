#!/usr/bin/env python3
"""Fetch official source URLs and compare raw response SHA-256 hashes.

The verifier intentionally stores no response bodies and contains no author
identity. It reports current observations to stdout as CSV.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


HEADERS = {
    "User-Agent": "source-traceability-verifier/1.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "identity",
}

FAILURE_RESULTS = {
    "mismatch",
    "fetch_error",
    "unfetchable_no_expected_hash",
    "fetch_error_no_expected_hash",
}


def pacific_now() -> str:
    return datetime.now(ZoneInfo("America/Vancouver")).replace(microsecond=0).isoformat()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, timeout: float) -> Dict[str, str]:
    request = Request(url, headers=HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            return {
                "http_status": str(response.status),
                "final_url": response.geturl(),
                "bytes": str(len(body)),
                "observed_sha256": sha256_hex(body),
                "error": "",
            }
    except HTTPError as exc:
        body = exc.read()
        return {
            "http_status": str(exc.code),
            "final_url": exc.geturl(),
            "bytes": str(len(body)),
            "observed_sha256": sha256_hex(body) if body else "",
            "error": f"HTTPError {exc.code}",
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "http_status": "",
            "final_url": url,
            "bytes": "0",
            "observed_sha256": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def classify(expected: str, observation: Dict[str, str]) -> str:
    expected = expected.strip().lower()
    observed = observation["observed_sha256"].strip().lower()
    status = observation["http_status"]
    error = observation["error"]

    if status and status.isdigit() and int(status) >= 400:
        return "fetch_error" if expected else "unfetchable_no_expected_hash"
    if error:
        return "fetch_error" if expected else "fetch_error_no_expected_hash"
    if not expected:
        return "observed_no_expected_hash"
    if not observed:
        return "fetch_error"
    if expected == observed:
        return "match"
    return "mismatch"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        default=Path(__file__).with_name("source_manifest.csv"),
        type=Path,
        help="Path to source_manifest.csv",
    )
    parser.add_argument("--timeout", default=30.0, type=float, help="Fetch timeout in seconds")
    args = parser.parse_args()

    with args.manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    fieldnames = [
        "citation_key",
        "result",
        "http_status",
        "bytes",
        "expected_sha256",
        "observed_sha256",
        "project_verifier_observed_at_pt",
        "final_url",
        "error",
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    observed_at = pacific_now()
    exit_code = 0
    for row in rows:
        observation = fetch(row.get("retrieval_url") or row["official_url"], args.timeout)
        result = classify(row.get("response_sha256", ""), observation)
        if result in FAILURE_RESULTS:
            exit_code = 1
        writer.writerow(
            {
                "citation_key": row["citation_key"],
                "result": result,
                "http_status": observation["http_status"],
                "bytes": observation["bytes"],
                "expected_sha256": row.get("response_sha256", ""),
                "observed_sha256": observation["observed_sha256"],
                "project_verifier_observed_at_pt": observed_at,
                "final_url": observation["final_url"],
                "error": observation["error"],
            }
        )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
