# app/Dockerfile
FROM python:3.9-slim
EXPOSE 5000
EXPOSE 8000
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python","app4.py" ]
