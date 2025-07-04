FROM python:3.9-slim
WORKDIR /home/forcloud
RUN pip install  paramiko pexpect requests PyYAML 
RUN mkdir -p /home/forcloud/POC-version-1.4
COPY scripts /home/forcloud/POC-version-1.4/scripts
COPY yamls /home/forcloud/POC-version-1.4/yamls
COPY kubectl /usr/bin/kubectl
RUN apt-get install -y netcat-traditional
CMD ["/bin/bash"]
