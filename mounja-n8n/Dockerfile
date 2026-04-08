FROM n8nio/n8n:latest

USER root

# Python + libs do sistema necessárias pro Pillow + onnxruntime (rembg)
RUN apk add --no-cache \
    python3 py3-pip \
    freetype jpeg zlib libpng tiff \
    libstdc++ libgomp \
    font-noto font-noto-extra ttf-dejavu \
    && python3 -m pip install --break-system-packages --no-cache-dir \
        pillow==10.4.0 \
        requests==2.32.3

# Scripts de composição + meta prompt + assets (logo, fontes)
COPY scripts/ /data/scripts/
COPY assets/ /data/assets/

# Diretório de runs (volume Railway monta aqui)
RUN mkdir -p /data/outputs && chown -R node:node /data

USER node
