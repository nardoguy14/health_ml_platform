FROM --platform=linux/amd64 nvcr.io/nvidia/pytorch:24.01-py3

ENV MYSQL_HOST=localhost
ENV MYSQL_USER=user
ENV MYSQL_PASS=pass
ENV MYSQL_DB=abc

RUN rm -rf /app \
    mkdir /app \
    chmod 777 /app

COPY ../app /app

WORKDIR /app

RUN pip install --upgrade pip; \
    pip install -r scripts/requirements.txt;

WORKDIR /

ENTRYPOINT ["python3", "-m", "app.scripts.run_job"]
