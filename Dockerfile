FROM kernsuite/base:5
LABEL maintainer=gijs@pythonic.nl
RUN docker-apt-install git
RUN echo "Test this stuff"
RUN docker-apt-install python3 python3-virtualenv
ARG NB_USER=rattru
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}
EXPOSE 8888
ENV VIRTUAL_ENV="${HOME}/nasspenv"
RUN python3 -m virtualenv -p /usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:${HOME}/.local/bin:$PATH"
RUN pip install --no-cache-dir -r ${HOME}/requirements.txt
WORKDIR ${HOME}