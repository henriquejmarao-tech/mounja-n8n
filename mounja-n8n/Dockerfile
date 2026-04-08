FROM n8nio/n8n:latest

USER root

# Python + libs do sistema necessárias pro Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip \
        libfreetype6 libjpeg62-turbo zlib1g libpng16-16 libtiff6 \
            libstdc++6 libgomp1 \
                fonts-noto fonts-noto-extra fonts-dejavu \
                 && python3 -m pip install --break-system-packages --no-cache-dir \
                     pillow==10.4.0 \
                         requests==2.32.3 \
                          && rm -rf /var/lib/apt/lists/*

                          # Scripts de composicao + meta prompt + assets (logo, fontes)
                          COPY scripts/ /data/scripts/
                          COPY assets/ /data/assets/

                          # Diretorio de runs (volume Railway monta aqui)
                          RUN mkdir -p /data/outputs && chown -R node:node /data

                          USER node
                          
