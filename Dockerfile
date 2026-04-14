ARG IMAGE=python
ARG IMAGE_TAG="3.14.4-alpine3.23"
FROM ${IMAGE}:${IMAGE_TAG}
WORKDIR /tmp
COPY ./pyproject.toml ./
RUN pip install --upgrade pip && pip install . --break-system-packages
ENV PORT=8080
ENV WSGI_DIR=/opt
ENV WSGI_APP=wsgi:application
COPY wsgi.py $WSGI_DIR
COPY main.py $WSGI_DIR
#CMD ["pip", "list"]
ENTRYPOINT gunicorn -b 0.0.0.0:$PORT -w 3 --access-logfile '-' --chdir $WSGI_DIR $WSGI_APP \
  --access-logformat '%({X-Forwarded-For}i)s %({Host}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
EXPOSE $PORT/tcp
