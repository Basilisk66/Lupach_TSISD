import datetime
import os
import shutil
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))

from ratelimiter import load_config  # noqa: E402


def main() -> int:
    public = os.path.join(ROOT, "public")
    os.makedirs(public, exist_ok=True)
    log_path = os.path.join(public, "deploy.log")

    def log(msg):
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        line = f"[{ts}] {msg}"
        print(line)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    src = os.path.join(ROOT, "config", "limits.json")
    log("deploy started")
    cfg = load_config(src)
    log(f"config valid: limit={cfg['limit']}, window={cfg['window_seconds']}s")
    shutil.copy(src, os.path.join(public, "limits.json"))
    log("limits.json copied to public/")
    log(f"commit: {os.environ.get('GITHUB_SHA', 'local')}")
    log("deploy finished successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
