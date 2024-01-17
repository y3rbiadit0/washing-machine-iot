FROM python:3.11-buster


RUN pip install poetry==1.7.1
WORKDIR /app
COPY . /app
RUN ["poetry", "install"]

EXPOSE 8000
ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--proxy-headers", "--reload", "--host", "0.0.0.0", "--port", "8000"]