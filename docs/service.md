# service

## Create the systemd-service

Change the path's below to fit your installation.
```bash
sudo nano /etc/systemd/system/optd-color.service
```
Paste below
```text
[Unit]
Description=OpenPrintTagDatabase Filament Search
After=network.target

[Service]
Type=simple
User=<user>
WorkingDirectory=/home/python/OpenPrintTagDatabase-Color-Search/
ExecStart=/home/python/OpenPrintTagDatabase-Color-Search/.venv/bin/python /home/python/OpenPrintTagDatabase-Color-Search/optdsearch.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
## Activate and start
```bash
sudo systemctl daemon-reload
sudo systemctl enable optd-color
sudo systemctl start optd-color
```
Logs
```bash
journalctl -u optd-color -f
```
Stop the service
```
sudo systemctl stop optd-color
```

Restart the service
```
sudo systemctl restart optd-color
```
