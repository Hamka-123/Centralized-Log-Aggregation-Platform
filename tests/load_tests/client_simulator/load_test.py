import os
import subprocess
import datetime
import sys
import time
import argparse

# 1. Define SCRIPT_DIR first so it's available globally
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Find project root dynamically
def find_project_root():
    current_dir = SCRIPT_DIR
    while True:
        if os.path.exists(os.path.join(current_dir, 'common')):
            return current_dir
        parent = os.path.dirname(current_dir)
        if parent == current_dir: # Reached filesystem root
            break
        current_dir = parent
    return None

PROJECT_ROOT = find_project_root()
if PROJECT_ROOT:
    sys.path.insert(0, PROJECT_ROOT)
else:
    print("Error: Could not find 'common' directory in the project tree.")
    sys.exit(1)

# Now it is safe to import
from common.config import Config

# 3. Configuration for report storage
REPORTS_DIR = os.path.join(SCRIPT_DIR, "reports")
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
REPORT_DIR = os.path.join(REPORTS_DIR, TIMESTAMP)
REPORT_FILE = os.path.join(REPORT_DIR, "report.html")

os.makedirs(REPORT_DIR, exist_ok=True)

def run(cmd, env_vars=None):
    """Execute a shell command with optional environment variables."""
    current_env = os.environ.copy()
    if env_vars:
        current_env.update(env_vars)
        
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=current_env)
    if result.returncode != 0:
        print(f"Error executing: {cmd}\n{result.stderr}")
    return result.stdout

def capture_stats(label):
    """Fetch docker stats and format them as an HTML table."""
    cmd = "docker stats --no-stream --format '<tr><td>{{.Name}}</td><td>{{.CPUPerc}}</td><td>{{.MemUsage}}</td></tr>'"
    stats = run(cmd)
    return f"<div class='card'><h2>{label}</h2><table><tr><th>Name</th><th>CPU</th><th>Mem</th></tr>{stats}</table></div>"

def main():
    parser = argparse.ArgumentParser(description="Log aggregation load test")
    
    parser.add_argument("--cleanup", action="store_true", help="Cleanup environment after test")
    parser.add_argument("--mailhog", action="store_true", help="Use MailHog for SMTP")
    parser.add_argument("--no-smtp", action="store_true", help="Disable SMTP")
    
    parser.add_argument("--clients", type=int, default=10, help="Number of clients to run (default: 10)")
    
    args = parser.parse_args()
    
    password = Config.DB_ROOT_PASSWORD
    html_content = ""
    
    cleanup = args.cleanup
    use_mailhog = args.mailhog
    no_smtp = args.no_smtp
    
    # 1. Determine the value for DISABLE_SMTP
    # If the --no-smtp flag is passed, force "true".
    # Otherwise, take it from the config (convert it to a string to pass to Docker).
    disable_smtp_val = "true" if no_smtp else str(Config.DISABLE_SMTP).lower()
    
    smtp_env_dict = {
        "SMTP_HOST": "mailhog" if use_mailhog else Config.SMTP_SERVER,
        "SMTP_PORT": "1025" if use_mailhog else str(Config.SMTP_PORT),
        "DISABLE_SMTP": "false" if use_mailhog else disable_smtp_val,
        "ENCRYPTION": "none" if use_mailhog else "STARTTLS"
    }
    
    print("--- Starting infrastructure ---")
    run("docker compose up -d --force-recreate api_collector db mailhog", env_vars=smtp_env_dict)
    
    print("--- Launching worker ---")
    run("docker compose rm -f alerting_worker")
    run("docker compose up -d --force-recreate alerting_worker", env_vars=smtp_env_dict)
    
    
    html_content += capture_stats("Baseline (Before Load)")

    print("--- Launching clients ---")
    count = args.clients
    print(f"--- Launching {count} clients using scaling ---")
    run("docker compose rm -f -s log-client")
    run(f"docker compose up -d --scale log-client={count} log-client")

    print("--- Running test for 60 seconds ---")
    time.sleep(60)
    
    html_content += capture_stats("Peak Load")

    print("--- Collecting DB metrics ---")
    # Using Config.DB_NAME from your existing configuration
    db_cmd = f"docker exec -i centralized_log_db mysql -u root -p'{password}' {Config.DB_NAME} < {SCRIPT_DIR}/kpi_report.sql"
    db_metrics = run(db_cmd)
    
    # Check if the metrics were retrieved successfully
    if db_metrics:
        html_content += f"<div class='card'><h2>Database Metrics</h2><pre>{db_metrics}</pre></div>"
    else:
        html_content += f"<div class='card'><h2>Database Metrics</h2><p>No data returned from DB.</p></div>"
        
    print("--- Cleaning up log clients ---")
    run("docker compose rm -f -s log-client")
    
    time.sleep(30)
    html_content += capture_stats("After Load (Recovery)")

    # 4. Generate the final HTML report from the template
    template_path = os.path.join(SCRIPT_DIR, "report_template.html")
    with open(template_path, "r") as f:
        template = f.read()
    
    final_html = template.replace("{timestamp}", TIMESTAMP).replace("{content}", html_content)
    
    with open(REPORT_FILE, "w") as f:
        f.write(final_html)

    print(f"Test complete. Report saved to: {REPORT_FILE}")
    
    if cleanup:
        print("--- Cleaning up environment ---")
        run("docker compose down -v")
    else:
        print("--- Infrastructure left running for inspection ---")

if __name__ == "__main__":
    main()