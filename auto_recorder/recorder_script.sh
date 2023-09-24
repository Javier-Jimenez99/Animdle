if pgrep "Xvfb" > /dev/null
then
    echo "Xvfb is running"
else
    rm -rf /tmp/.X1-lock
fi

nohup Xvfb :1 -screen 0 594x1056x24 +extension RANDR &

pulseaudio --start --load=module-native-protocol-tcp --exit-idle-time=-1

python auto_recorder.py --data-dir parsed_data