#FROM python:3.9.2
FROM python:slim
WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
RUN pip3 install --upgrade pip

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN rm -rf venv
COPY venv/Lib/site-packages/instabot venv/Lib/site-packages/instabot

CMD ["python","./main.py"]