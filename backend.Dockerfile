FROM python:3.11-slim

WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.linux.txt requirements.txt
COPY requirements.linux.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

COPY app.py .
COPY detection_methods/ detection_methods/

EXPOSE 5001

CMD ["python", "app.py"]
