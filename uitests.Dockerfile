FROM python:3.7-buster
WORKDIR /usr/src/app
COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh
RUN pip install behave==1.2.6
RUN pip install allure-behave==2.8.24
RUN pip install selenium==3.141.0
COPY . .
CMD behave