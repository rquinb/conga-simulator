FROM python:3.7-buster as unit-tests
WORKDIR /usr/src/app
COPY requirements.txt ./requirements.txt
RUN pip install virtualenv
RUN virtualenv conga-env
RUN . conga-env/bin/activate && pip install --no-cache-dir -r requirements.txt
COPY .coverage-config ./.coverage-config
COPY entities/ ./entities
COPY *py ./
COPY tests/ ./tests/
RUN . conga-env/bin/activate && python -m pytest -v --cov-report term --cov=. --cov-config=.coverage-config tests/

FROM python:3.7-buster
WORKDIR /usr/src/app
COPY --from=unit-tests /usr/src/app/conga-env ./conga-env
COPY entities/ ./entities
COPY . ./
CMD . conga-env/bin/activate && python ./app.py
