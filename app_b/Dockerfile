FROM python:3.10-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app_b /app
CMD ["python", "main.py"]
