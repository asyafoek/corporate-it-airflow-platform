
nerdctl stop dagger-engine-v0.20.0 2>/dev/null || true
nerdctl rm   dagger-engine-v0.20.0 2>/dev/null || true


VER="v0.20.0"   # use the same version as your Python SDK
nerdctl run -d --restart=always --privileged \
  --name dagger-engine-${VER} \
  -v dagger-engine:/var/lib/dagger \
  registry.dagger.io/engine:${VER}

export _EXPERIMENTAL_DAGGER_RUNNER_HOST="container+nerdctl://dagger-engine-${VER}"

# export GHCR_TOKEN=...

python dagger_build.py