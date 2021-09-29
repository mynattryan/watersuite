# watersuite
A collection of simple python scripts to achieve some level of automation in our pump house. Uses an old first gen Raspberry Pi with various sensors connected.

\*.service files should be copied to /etc/systemd/system and loaded with:
```
sudo systemctl daemon-reload
sudo systemctl enable <service>
sudo systemctl start <service>
```
