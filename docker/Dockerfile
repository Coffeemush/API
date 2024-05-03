FROM python:3.8-alpine
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        libffi-dev
WORKDIR /api
COPY . /api
RUN pip install -r /api/docker/requirements.txt
ENTRYPOINT [ "python" ]
CMD ["app.py" ]