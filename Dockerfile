FROM python:3.11.9-slim

RUN mkdir /project_helper

WORKDIR /project_helper

ENV VIRTUAL_ENV=/project_helper/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./pyproject.toml poetry.lock alembic.ini /project_helper/

RUN python -m pip install --upgrade pip

RUN pip install poetry

RUN poetry install

COPY ./app /project_helper/app

ENV PYTHONPATH "${PYTHONPATH}:/project_helper/app"

RUN chmod a+x /project_helper/app/scripts/start.sh

# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
