FROM python:3.12-slim

ARG REPO_URL=https://github.com/dzCazador/ITS-DevOps-Lab2-SitioBancoPython.git
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN git clone "$REPO_URL" . && rm -rf .git

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8555

CMD ["python", "main.py"]
