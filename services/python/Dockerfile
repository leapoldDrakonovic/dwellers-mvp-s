FROM python:3.10-slim-buster

RUN apt-get update \
  # install curl
  && apt-get -y install curl \
  # install utils
  && apt-get install xz-utils \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Download latest nodejs binary
# RUN curl https://nodejs.org/dist/v20.3.1/node-v20.3.1-linux-x64.tar.xz -O
# Extract & install
# RUN tar -xf ../node-v20.3.1-linux-x64.tar.xz
# RUN ln -s /node-v20.3.1-linux-x64/bin/node /usr/local/bin/node
# RUN ln -s /node-v20.3.1-linux-x64/bin/npm /usr/local/bin/npm
# RUN ln -s /node-v20.3.1-linux-x64/bin/npx /usr/local/bin/npx

# RUN npm init -y
# RUN npm install webpack webpack-cli --save-dev

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./services/python/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./services/python/start-flask /start-flask
RUN sed -i 's/\r$//g' /start-flask
RUN chmod +x /start-flask

COPY ./web /web
WORKDIR /web

ENTRYPOINT [ "/entrypoint" ]
