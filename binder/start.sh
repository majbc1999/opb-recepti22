#!/bin/bash
export BOTTLE_PORT=8080
export BOTTLE_RELOADER=1
export BOTTLE_ROOT=${JUPYTERHUB_SERVICE_PREFIX}proxy/${BOTTLE_PORT}/
export BOTTLE_RUNTIME=spletni_vmesnik.py
export POSTGRES_PORT=443
python ${BOTTLE_RUNTIME} &
exec "$@"