FROM 'python:3.11'

WORKDIR /code

COPY . /code
# COPY ./python-lib.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/python-lib.txt

COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# docker build -t rejs/github-sub:latest .