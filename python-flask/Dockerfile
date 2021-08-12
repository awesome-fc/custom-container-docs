FROM python:3.9.0-slim

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .

CMD [ "python", "-u", "./app.py" ]
