FROM python:3.12-slim as builder

RUN pip install poetry
RUN mkdir -p /app
COPY . /app

WORKDIR /app
# install a virtual env in the docker image
RUN poetry config virtualenvs.in-project true --local
# ignore dev dependencies
RUN poetry install --without dev

FROM python:3.12-slim as base

COPY --from=builder /app /app

WORKDIR /app/pg_pfmon
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "main"]