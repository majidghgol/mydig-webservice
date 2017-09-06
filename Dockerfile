# mydig-webservice
FROM uscisii2/etk:1.0.0

# all packages and environments are in /app
WORKDIR /app
RUN mkdir /app/mydig-webservice

# install dependencies of mydig
ADD requirements.txt /app/mydig-webservice
RUN pip install -r /app/mydig-webservice/requirements.txt

# persistent data
#VOLUME /shared_data
RUN mkdir /shared_data

EXPOSE 9879
EXPOSE 9880

# mydig-webservice
ADD . /app/mydig-webservice
RUN mv /app/mydig-webservice/dig3-resources /shared_data/dig3-resources
RUN ln -sf /app/mydig-webservice/ws/config_docker.py /app/mydig-webservice/ws/config.py
CMD chmod +x /app/mydig-webservice/docker_run_mydig.sh && \
    /bin/bash -c "/app/mydig-webservice/docker_run_mydig.sh"
