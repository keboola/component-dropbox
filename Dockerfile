FROM python:3.13-slim
ENV PYTHONIOENCODING=utf-8

RUN apt-get update && apt-get install -y build-essential

RUN pip install uv

COPY pyproject.toml /code/pyproject.toml
COPY uv.lock /code/uv.lock

WORKDIR /code

RUN uv pip sync /code/uv.lock

COPY /src /code/src/
COPY /tests /code/tests/
COPY /scripts /code/scripts/
COPY deploy.sh /code/deploy.sh

COPY pyproject.toml /code/

CMD ["python", "-u", "/code/src/component.py"]
