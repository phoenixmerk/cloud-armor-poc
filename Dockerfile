FROM python:3.9-slim
WORKDIR /home/forcloud
RUN pip install  paramiko pexpect requests PyYAML -i https://pypi.mirrors.ustc.edu.cn/simple 
COPY /home/circleci/project/kubectl /usr/bin/kubectl
COPY /home/circleci/project/netcat-traditional_1.10-41.1_amd64.deb /home/forcloud/netcat-traditional_1.10-41.1_amd64.deb
RUN dpkg -i /home/forcloud/netcat-traditional_1.10-41.1_amd64.deb && rm -f /home/forcloud/netcat-traditional_1.10-41.1_amd64.deb
CMD ["/bin/bash"]
