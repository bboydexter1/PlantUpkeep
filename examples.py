[Unit]
Description=plant upkeep system service
After=multi-user.target
[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/Farma/main.py
[Install]
WantedBy=multi-user.target

mv /lib/systemd/system/plantUpkeep  /lib/systemd/system/plant.upkeep
