FROM python:3.6.3
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip cython && pip install -r requirements.txt
# Generate usernames
RUN for i in $(seq 10000 10999); do \
  echo "user$i:x:$i:$i::/tmp:/usr/sbin/nologin" >> /etc/passwd; \
  done
COPY . /app
RUN mkdir -p /app/datasets
RUN chmod -R 755 /app
RUN chmod -R 777 static images templates datasets app.py
ENTRYPOINT ["python3" ]
CMD ["app.py"]
