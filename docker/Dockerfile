# syntax=docker/dockerfile:1.7
ARG ROS_DISTRO=jazzy

# ───────────────────────── base ─────────────────────────
# Sistema + usuario no-root con el MISMO uid/gid que el host.
FROM ros:${ROS_DISTRO}-ros-base AS base
ARG ROS_DISTRO
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DISTRO=${ROS_DISTRO} \
    WS=/workspaces/ros2_demo
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
 && apt-get install -y --no-install-recommends sudo \
 && rm -rf /var/lib/apt/lists/* \
 && if getent group "${USER_GID}" >/dev/null; then \
        groupmod -n "${USERNAME}" "$(getent group "${USER_GID}" | cut -d: -f1)"; \
    else \
        groupadd --gid "${USER_GID}" "${USERNAME}"; \
    fi \
 && if getent passwd "${USER_UID}" >/dev/null; then \
        usermod -l "${USERNAME}" -d "/home/${USERNAME}" -m \
          "$(getent passwd "${USER_UID}" | cut -d: -f1)"; \
    else \
        useradd --uid "${USER_UID}" --gid "${USER_GID}" -m "${USERNAME}"; \
    fi \
 && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
 && chmod 0440 /etc/sudoers.d/${USERNAME}

# Estos directorios deben existir Y pertenecer al usuario ANTES de que
# Compose monte volúmenes nombrados encima (si no, quedan root:root).
RUN mkdir -p ${WS}/src ${WS}/build ${WS}/install ${WS}/log \
 && chown -R ${USER_UID}:${USER_GID} /workspaces

# ───────────────────────── deps ─────────────────────────
# Solo el manifiesto: si package.xml no cambia, rosdep no se repite.
FROM base AS deps
WORKDIR ${WS}
COPY src/demo_chatter/package.xml src/demo_chatter/package.xml

RUN apt-get update \
 && rosdep update --rosdistro ${ROS_DISTRO} \
 && rosdep install --from-paths src --ignore-src -y --rosdistro ${ROS_DISTRO} \
 && rm -rf /var/lib/apt/lists/*

# ───────────────────────── dev ──────────────────────────
# Entorno interactivo. NO copia el código: se monta por volumen.
FROM deps AS dev
ARG ROS_DISTRO
ARG USERNAME=dev

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      bash-completion git vim less \
      iproute2 iputils-ping net-tools \
      python3-pip \
      ros-${ROS_DISTRO}-rqt-graph \
 && rm -rf /var/lib/apt/lists/*

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER ${USERNAME}
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc \
 && echo "[ -f ${WS}/install/setup.bash ] && source ${WS}/install/setup.bash" >> ~/.bashrc \
 && echo 'export PS1="🐳 \[\e[36m\]\u@ros2-demo\[\e[0m\]:\w\$ "' >> ~/.bashrc

WORKDIR ${WS}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]

# ──────────────────────── build ─────────────────────────
# Compilación real, aislada. Nada de esto llega a la imagen final.
FROM deps AS build
COPY src/ ${WS}/src/
WORKDIR ${WS}
RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
 && colcon build --merge-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# ─────────────────────── runtime ────────────────────────
# Solo dependencias de EJECUCIÓN + el install/ compilado.
FROM base AS runtime
ARG ROS_DISTRO
ARG USERNAME=dev

WORKDIR ${WS}
COPY src/demo_chatter/package.xml src/demo_chatter/package.xml
RUN apt-get update \
 && rosdep update --rosdistro ${ROS_DISTRO} \
 && rosdep install --from-paths src --ignore-src -y \
      --rosdistro ${ROS_DISTRO} --dependency-types=exec \
 && rm -rf /var/lib/apt/lists/* ${WS}/src

COPY --from=build --chown=${USERNAME}:${USERNAME} ${WS}/install ${WS}/install
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER ${USERNAME}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["ros2", "launch", "demo_chatter", "demo.launch.py"]
