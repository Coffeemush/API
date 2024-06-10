FROM python:3.8-alpine
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        libffi-dev
WORKDIR /api
COPY docker/requirements.txt /api/docker/requirements.txt
RUN pip install -r /api/docker/requirements.txt
COPY . /api
ENTRYPOINT [ "python" ]
CMD ["app.py" ]