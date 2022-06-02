FROM python:3.10

WORKDIR /code

COPY . .

ENTRYPOINT [ "python", "main.py" ]
