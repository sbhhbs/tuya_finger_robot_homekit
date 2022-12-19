FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/root/app
WORKDIR /root/app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
