FROM n8nio/n8n:latest
USER root
RUN export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH" && if command -v apk >/dev/null 2>&1; then apk add --no-cache python3 py3-pip py3-pillow py3-requests ttf-dejavu font-noto; elif command -v apt-get >/dev/null 2>&1; then apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-pil python3-requests fonts-dejavu fonts-noto && rm -rf /var/lib/apt/lists/*; else echo "no pkg mgr" && cat /etc/os-release && exit 1; fi
COPY scripts/ /data/scripts/
COPY assets/ /data/assets/
RUN mkdir -p /data/outputs && chown -R node:node /data
USER node
