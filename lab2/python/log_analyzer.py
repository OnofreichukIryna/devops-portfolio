import argparse
import re
from collections import Counter
from datetime import datetime

def parse_line(line):
    # Regex for standard Nginx/Apache log format
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>.*?)" "(?P<user_agent>.*?)"')
    match = pattern.match(line)
    return match.groupdict() if match else None

def analyze(log_path):
    ip_counts = Counter()
    status_counts = Counter()
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                data = parse_line(line)
                if data:
                    ip_counts[data['ip']] += 1
                    status_counts[data['status']] += 1
        return ip_counts, status_counts
    except FileNotFoundError:
        print("Error: Log file not found")
        return None, None

def generate_report(ips, statuses):
    # Simple HTML template
    html = f"""
    <html>
    <head><title>Log Report</title></head>
    <body>
        <h1>Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}</h1>
        
        <h2>Top 5 IPs</h2>
        <ul>
        {''.join([f'<li>{ip}: {count} requests</li>' for ip, count in ips.most_common(5)])}
        </ul>
        
        <h2>Status Codes</h2>
        <ul>
        {''.join([f'<li>Code {code}: {count} times</li>' for code, count in statuses.items()])}
        </ul>
    </body>
    </html>
    """
    with open("report.html", "w") as f:
        f.write(html)
    print("Done. Report saved to report.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse web logs")
    parser.add_argument("logfile", help="Path to log file")
    args = parser.parse_args()
    
    ips, statuses = analyze(args.logfile)
    if ips:
        generate_report(ips, statuses)