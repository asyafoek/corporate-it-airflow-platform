#!/usr/bin/env python3
import anyio
import dagger
import os
import sys
import subprocess
from pathlib import Path

# Keep your original paths/flags exactly as-is
NAMESPACE       = "corporate-it-airflow"
API_SECRET_FILE = "src/resources/secrets/my-api-secret.yaml"
HELM_CMD        = (
    "helm upgrade --install airflow src/resources/airflow "
    "--namespace corporate-it-airflow "
    "-f src/resources/airflow/values.yaml "
    "--debug"
)

def run(cmd: str):
    """Run a shell command on the host and stream output; raise on failure."""
    print(f"\n$ {cmd}")
    subprocess.check_call(cmd, shell=True)

async def main():
    # Establish a Dagger session (no container usage; just to conform to your requirement)
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as _client:
        # (Optional) quick sanity checks; safe to remove if you prefer
        if not Path(API_SECRET_FILE).exists():
            print(f"[ERR] Secret file not found: {API_SECRET_FILE}", file=sys.stderr)
            sys.exit(1)

        # 1) Ensure namespace exists (exact command)
        run(f"kubectl get namespace {NAMESPACE} || kubectl create namespace {NAMESPACE}")

        # 2) Apply API secret (exact command)
        run(f"kubectl apply -f {API_SECRET_FILE}")


        # 3) Deploy Helm release (EXACT command you specified)
        run(HELM_CMD)

        print("\n[OK] Secret applied, namespace ensured, Helm release deployed (using your exact Helm command).")

if __name__ == "__main__":
    anyio.run(main)