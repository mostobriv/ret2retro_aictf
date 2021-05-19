FROM python:3.7

WORKDIR /opt/ret2retro/
COPY glitcher/setup.py /opt/glitcher/
COPY nn/setup.py /opt/nn/
COPY web/setup.py /opt/ret2retro/

RUN pip install -e ../glitcher && \
    pip install -e ../nn && \
    pip install -e .

RUN pip uninstall -y h5py
RUN pip install h5py==2.10.0

COPY ./nn/nn /opt/nn/nn
COPY ./glitcher/glitcher /opt/glitcher/glitcher

COPY ./web/ret2retro /opt/ret2retro/ret2retro
COPY ./web/static /opt/ret2retro/static

COPY flag.txt /flag.txt

EXPOSE 80

CMD ["python", "-m", "ret2retro"]
