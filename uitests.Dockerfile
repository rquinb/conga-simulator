FROM python:3.7-buster
WORKDIR /usr/src/app
COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh
RUN pip install behave
RUN pip install selenium
COPY . .
CMD behave