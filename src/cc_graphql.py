# Adapted from: vinebloom-flower-overlay/src/add_variants.py (GraphQL pattern)
"""
CloudCart GraphQL API helper for Owllee migration.
Wraps all API calls with rate limiting and error handling.
"""

import json
import time
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

from config import CC_GQL_URL, CC_PAT_TOKEN

HEADERS = {
    "Authorization": f"Bearer {CC_PAT_TOKEN}",
    "Content-Type": "application/json",
}

# Rate limiting: CloudCart allows ~50 req/min on GraphQL
CALLS_SINCE_PAUSE = 0
MAX_CALLS_PER_BATCH = 45
PAUSE_SECONDS = 62


def gql(query, variables=None, retries=3):
    """Execute a GraphQL query/mutation with rate limiting and retries."""
    global CALLS_SINCE_PAUSE

    if CALLS_SINCE_PAUSE >= MAX_CALLS_PER_BATCH:
        print(f"    [rate limit] pausing {PAUSE_SECONDS}s...")
        time.sleep(PAUSE_SECONDS)
        CALLS_SINCE_PAUSE = 0

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(retries):
        try:
            resp = requests.post(CC_GQL_URL, headers=HEADERS, json=payload, timeout=30)
            CALLS_SINCE_PAUSE += 1

            if resp.status_code == 429:
                wait = 65
                print(f"    [429] rate limited, waiting {wait}s...")
                time.sleep(wait)
                CALLS_SINCE_PAUSE = 0
                continue

            data = resp.json()

            if "errors" in data:
                errors = data["errors"]
                msg = errors[0].get("message", str(errors))
                if attempt < retries - 1:
                    print(f"    [error] {msg} — retrying ({attempt+1}/{retries})")
                    time.sleep(2)
                    continue
                return {"errors": errors, "data": data.get("data")}

            return data

        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                print(f"    [network error] {e} — retrying ({attempt+1}/{retries})")
                time.sleep(5)
                continue
            raise

    return {"errors": [{"message": "max retries exceeded"}]}


def reset_rate_counter():
    global CALLS_SINCE_PAUSE
    CALLS_SINCE_PAUSE = 0
