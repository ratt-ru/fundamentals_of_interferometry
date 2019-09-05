FROM kernsuite/base:5
MAINTAINER gijs@pythonic.nl
RUN docker-apt-install python3 python3-pip
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /notebooks
EXPOSE 8888
WORKDIR /notebooks
CMD jupyter notebook --ip 0.0.0.0  --notebook-dir=/notebooks
