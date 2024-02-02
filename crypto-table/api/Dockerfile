FROM python:3.8-slim

WORKDIR /api

COPY . /api

RUN pip install flask requests

EXPOSE 8888

CMD ["python", "app.py"]
