FROM registry.access.redhat.com/ubi10/python-312-minimal:10.0-1747316123

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./akka .

EXPOSE 5000

CMD ["python", "main.py"]
