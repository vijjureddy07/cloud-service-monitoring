FROM python:3.12-slim
WORKDIR /service
COPY app/ ./app/
RUN useradd -m -u 10001 appuser
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz',timeout=3)"
CMD ["python", "-m", "app.server"]
