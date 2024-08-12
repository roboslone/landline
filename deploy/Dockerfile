FROM python:3 AS minimal

RUN python3 -m pip install --upgrade pip typed_settings requests attrs
RUN python3 -m pip install git+https://github.com/openai/whisper.git

RUN mkdir -p /landline
ADD landline /landline

WORKDIR /
CMD ["python3", "/landline/main.py"]

FROM minimal AS full
RUN python3 /landline/main.py --preload-only
