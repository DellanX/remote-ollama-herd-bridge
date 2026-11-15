FROM ollama/ollama:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    pip3 install --break-system-packages ollama-herd

COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]