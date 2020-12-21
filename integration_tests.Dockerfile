FROM python:3.7-buster
WORKDIR /usr/src/app
COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh
COPY integration_tests_requirements.txt ./integration_tests_requirements.txt
RUN pip install -r integration_tests_requirements.txt
COPY test_api/ ./test_api
COPY features/ ./features
CMD behave