FROM python:3.13.1
LABEL maintainer="CastCris author"
RUN useradd -ms /bin/sh -u 1001 app

USER app

#
ENV workdir /app
WORKDIR ${workdir}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . /app

#
EXPOSE 5000
CMD [ "python3", "app.py" ]
