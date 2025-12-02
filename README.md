# USBIP Server
This python package helps to attach to USB devices on remote machines to local PCs over a webserver. The USB devices connected to the webserver can then be bound to the IP access over REST APIs. 

## Setting up USB over IP in ubuntu server machine 

Execute the below commands 

```bash

sudo apt install linux-tools-$(uname -r)

sudo modprobe usbip_core
sudo modprobe usbip_host

```
Edit the USB IP config file 

```bash

sudo nano /etc/modules-load.d/usbip.conf
```
Add the below lines there 

```text
usbip_core
usbip_host
```

if you want to permanantly run the USBIP daemon on every start up, configure the systemd service as below 

```bash
sudo nano /etc/systemd/system/usbipd.service

```text

Add the below text in the file 
```
[Unit]
Description=USB/IP server
After=network.target

[Service]
ExecStart=/usr/bin/usbipd

[Install]
WantedBy=multi-user.target
```
Finally run the service by 

```bash 
sudo systemctl enable --now usbipd.service
```

Now the USB over IP Daemon runs on every startup of the PC automatically , in this case you may not require the start end point use in the webserver. 


## Setting up the USBIP helper script
copy the file `usbip_helper.sh` to `/usr/local/bin/usbip_helper.sh`
```bash
sudo cp ./usbip_helper.sh /usr/local/bin/usbip_helper.sh
sudo chown root:root /usr/local/bin/usbip_helper.sh
sudo chmod 700 /usr/local/bin/usbip_helper.sh
 
```

change the sudoers list such that the invocation of the usbip commands does not require the password entry from user

```bash
sudo visudo
```

add the below line in to the opened file 

```text
user_name ALL=(root) NOPASSWD: /usr/local/bin/usbip_helper.sh

```
where `user_name` is the local non sudo user name with which this python tool will be executed



