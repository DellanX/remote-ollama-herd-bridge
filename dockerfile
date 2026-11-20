FROM vastai/base-image:cuda-13.4.2-auto

ENV OLLAMA_HOST=0.0.0.0:11434

RUN curl -fsSL https://ollama.com/install.sh | sh

EXPOSE 11434

CMD ["ollama", "serve"]