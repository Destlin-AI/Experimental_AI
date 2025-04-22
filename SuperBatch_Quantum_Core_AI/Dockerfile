
FROM nvidia/cuda:12.2-base
RUN apt-get update && apt-get install -y python3.10 python3-pip
COPY quantum_*.py /app
CMD ["python3", "-u", "/app/quantum_core.py"]
