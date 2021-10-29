FROM python:3.7

COPY . /app/

RUN apt-get update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r app/requirments.txt

EXPOSE 8080
CMD ["python", "/app/main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

