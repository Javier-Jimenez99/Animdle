if pgrep "Xvfb" > /dev/null
then
    echo "Xvfb is running"
else
    rm -rf /tmp/.X1-lock
fi

nohup Xvfb :1 -screen 0 594x1056x24 +extension RANDR &

# Cleanup to be "stateless" on startup, otherwise pulseaudio daemon can't start
rm -rf /var/run/pulse /var/lib/pulse /root/.config/pulse
pulseaudio --start --load=module-native-protocol-tcp --exit-idle-time=-1

/usr/local/bin/python /app/auto_recorder.py --data-dir /app/parsed_data --videos-folder /app/videos