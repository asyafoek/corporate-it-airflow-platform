import anyio
import dagger
import os
import sys

# --- Config ---
GITHUB_USER = "asyafoek"
IMAGE_NAME = "custom-airflow"
IMAGE_TAG = "latest"
DOCKER_CTX = "docker/airflow"

CHART_PATH = "./charts/airflow"          # lokale chart dir of .tgz
VALUES = "deploy/airflow/values.yaml"
NAMESPACE = "airflow"
RELEASE = "airflow"

# --- Feature toggles (env) ---
SKIP_BUILD  = os.environ.get("SKIP_BUILD",  "false").lower() in ("1","true","yes","y")
SKIP_DEPLOY = os.environ.get("SKIP_DEPLOY", "false").lower() in ("1","true","yes","y")

async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        image_ref = f"ghcr.io/{GITHUB_USER}/{IMAGE_NAME}:{IMAGE_TAG}"

        # -------- STAP 1: Build + Push (optioneel) --------
        if not SKIP_BUILD:
            build = client.host().directory(DOCKER_CTX).docker_build()
            ghcr = client.set_secret("ghcr", os.environ["GHCR_TOKEN"])
            await build.with_registry_auth("ghcr.io", GITHUB_USER, ghcr).publish(image_ref)
            print(f"[BUILD] pushed {image_ref}")
        else:
            print("[BUILD] overgeslagen")

        # -------- STAP 2: Deploy lokale Helm chart (optioneel) --------
        if not SKIP_DEPLOY:
            kube = client.set_secret("kubeconfig", os.environ["KUBECONFIG_CONTENTS"])
            runner = (
                client.container()
                .from_("dtzar/helm-kubectl:latest")
                .with_env_variable("KUBECONFIG", "/root/.kube/config")
                .with_secret_variable("KUBEFILE", kube)
                .with_exec(["/bin/sh","-lc",'mkdir -p /root/.kube && echo "$KUBEFILE" > /root/.kube/config'])
                .with_mounted_directory("/app", client.host().directory("."))
                .with_workdir("/app")
            )
            await runner.with_exec([
                "helm", "upgrade", "--install", RELEASE, CHART_PATH,
                "-n", NAMESPACE, "--create-namespace",
                "-f", VALUES,
                "--atomic", "--wait"
            ]).stdout()
            print("[DEPLOY] local chart deployed")
        else:
            print("[DEPLOY] overgeslagen")

anyio.run(main())