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

FROM python:3.7-buster as lint
WORKDIR /usr/src/app
RUN pip install pylint
COPY entities/ ./entities
COPY *py ./
COPY .pylintrc ./.pylintrc
RUN pylint app.py entities --rcfile=.pylintrc --fail-under 10 

FROM python:3.7-buster as complexity-analysis
WORKDIR /usr/src/app
RUN pip install radon
RUN pip install xenon
COPY --from=lint /usr/src/app/ ./
RUN radon cc . -a
RUN xenon . --max-absolute B --max-modules A --max-average A


FROM python:3.7-buster
WORKDIR /usr/src/app
COPY --from=unit-tests /usr/src/app/conga-env ./conga-env
COPY entities/ ./entities
COPY . ./
CMD . conga-env/bin/activate && python ./app.py
