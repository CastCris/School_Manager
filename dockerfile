FROM python:3.13.1
LABEL maintainer="CasCris author"

#
ENV workdir /DockerImage

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#
EXPOSE 5000
CMD [ "python3", "app.py" ]
