FROM python:3

WORKDIR /usr/src/app

COPY code/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY code/test.py .

CMD [ "python", "./test.py" ]
