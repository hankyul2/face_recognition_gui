FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-devel

ENV PATH=/opt/conda/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get -y upgrade && apt-get install -y python3-pip
RUN apt-get install -y wget
RUN python -m pip install --upgrade pip
RUN python -m pip install

WORKDIR /root

EXPOSE 5000
ENTRYPOINT [ "python", "app.py"]
