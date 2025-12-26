ARG IMAGE=python
ARG IMAGE_TAG="3.14-alpine"
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
ENTRYPOINT gunicorn -b 0.0.0.0:$PORT -w 3 --access-logfile '-' --chdir $WSGI_DIR $WSGI_APP
EXPOSE $PORT/tcp
