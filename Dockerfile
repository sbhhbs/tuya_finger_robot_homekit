FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/root/app
ENV FLASK_APP=app.py
WORKDIR /root/app
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:4000", "tv:app"]