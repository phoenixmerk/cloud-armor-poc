FROM python:3.9-slim
WORKDIR /home/forcloud
RUN pip install  paramiko pexpect requests PyYAML 
RUN mkdir -p /home/forcloud/POC-version-1.4
COPY scripts /home/forcloud/POC-version-1.4
COPY yamls /home/forcloud/POC-version-1.4
COPY kubectl /usr/bin/kubectl
COPY netcat-traditional_1.10-41.1_amd64.deb /home/forcloud/netcat-traditional_1.10-41.1_amd64.deb
RUN dpkg -i /home/forcloud/netcat-traditional_1.10-41.1_amd64.deb && rm -f /home/forcloud/netcat-traditional_1.10-41.1_amd64.deb
CMD ["/bin/bash"]
