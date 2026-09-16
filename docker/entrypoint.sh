#!/usr/bin/env bash
# Los scripts de setup de ROS no son compatibles con `set -u`,
# por eso solo usamos -e y pipefail.
set -eo pipefail

# 1) Entorno base de ROS
source "/opt/ros/${ROS_DISTRO}/setup.bash"

# 2) Overlay del workspace, si ya fue compilado
if [ -f "${WS}/install/setup.bash" ]; then
  source "${WS}/install/setup.bash"
fi

# 3) Ceder el PID 1 al comando pedido
exec "$@"
