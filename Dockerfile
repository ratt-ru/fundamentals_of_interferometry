FROM radioastro/python

MAINTAINER gijs@pythonic.nl

RUN apt-get update && apt-get install -yq --no-install-recommends \
    libpng-dev \
    libncurses5-dev \
    pkg-config \
    libfreetype6-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

RUN pip install numpy==1.10.1

RUN pip install -r /requirements.txt

COPY . /notebooks

RUN useradd notebook -m

RUN chown -R notebook /notebooks

EXPOSE 8888

WORKDIR /notebooks

USER notebook

CMD jupyter notebook --ip 0.0.0.0  --notebook-dir=/notebooks
