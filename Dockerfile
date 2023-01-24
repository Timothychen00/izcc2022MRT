FROM python:3.8
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python app.py