import requests
import time
import json
import csv
from datetime import datetime

# Config
ENDPOINTS = [
    "https://www.google.com",
    "https://www.github.com",
    "https://httpstat.us/404",  # Спеціально бите посилання для тесту
]
# Встав сюди свій вебхук від Discord
WEBHOOK_URL = "ТВІЙ_WEBHOOK_ТУТ"
OUTPUT_FILE = "monitor_results"


def send_alert(message):
    if "WEBHOOK" in WEBHOOK_URL:
        return  # Skip if not configured

    payload = {"content": f"🚨 **API Monitor Alert**\n{message}"}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Alert failed: {e}")


def check_sites():
    results = []
    print("Starting checks...")

    for url in ENDPOINTS:
        start_time = time.time()
        status = "DOWN"
        code = 0

        try:
            response = requests.get(url, timeout=5)
            code = response.status_code
            if 200 <= code < 400:
                status = "UP"
        except requests.RequestException:
            pass  # Site is down

        latency = round(time.time() - start_time, 3)

        # Log to console
        print(f"[{status}] {url} - {code} ({latency}s)")

        if status == "DOWN" or code >= 400:
            send_alert(f"Service {url} responded with {code}")

        results.append({
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "status": status,
            "code": code,
            "latency": latency
        })

    return results


def save_to_files(data):
    # Save JSON
    with open(f"{OUTPUT_FILE}.json", "w") as f:
        json.dump(data, f, indent=4)

    # Save CSV
    if data:
        with open(f"{OUTPUT_FILE}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    print(f"Results saved to {OUTPUT_FILE}.json and .csv")


if __name__ == "__main__":
    data = check_sites()
    save_to_files(data)
