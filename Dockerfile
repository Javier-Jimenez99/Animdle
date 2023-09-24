FROM python:3.9-slim

# xvfb & ffmpeg 
RUN apt-get update && \
    apt-get install -y xvfb ffmpeg pulseaudio imagemagick

# modify ImageMagick policy file so that Textclips work correctly.
RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml 

# Google Chrome
RUN apt-get install -y wget unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

RUN google-chrome --version

# ChromeDriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.88/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver-linux64.zip

COPY auto_recorder/* /app/
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY animdle_back/api/scripts/parsed_data/ /app/parsed_data/

WORKDIR /app

CMD ["bash", "recorder_script.sh"]
