FROM python:3.9.23-slim-bullseye
WORKDIR /home/forcloud
RUN pip install  paramiko pexpect requests PyYAML 
RUN mkdir -p /home/forcloud/POC-version-1.4
COPY scripts /home/forcloud/POC-version-1.4/scripts
COPY yamls /home/forcloud/POC-version-1.4/yamls
COPY kubectl /usr/bin/kubectl
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y netcat-traditional
CMD ["/bin/bash"]
