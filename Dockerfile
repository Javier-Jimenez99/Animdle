FROM python:3.9-slim

# xvfb & ffmpeg 
RUN apt-get update && \
    apt-get install -y xvfb ffmpeg pulseaudio imagemagick cron rsyslog wget unzip

# modify ImageMagick policy file so that Textclips work correctly.
RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml 

# Chromium
RUN apt-get install -y chromium

# Driver
RUN apt-get install chromium-driver

COPY auto_recorder/* /app/
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY animdle_back/api/scripts/parsed_data/ /app/parsed_data/

#RUN crontab -l | { cat; echo "* * * * * bash /app/recorder_script.sh >> /var/log/recorder_script.log"; } | crontab -

WORKDIR /app

CMD bash /app/recorder_script.sh
