FROM python:3.11-slim
WORKDIR /app
COPY controller.py .
RUN pip install paho-mqtt
CMD ["python", "controller.py"]
