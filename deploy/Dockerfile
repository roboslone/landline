FROM python:3 AS build

RUN apt -y update && apt -y install ffmpeg

RUN python3 -m pip install --upgrade pip typed_settings requests attrs
RUN python3 -m pip install git+https://github.com/openai/whisper.git

RUN mkdir -p /landline
ADD landline /landline

WORKDIR /
CMD ["python3", "/landline/main.py"]
