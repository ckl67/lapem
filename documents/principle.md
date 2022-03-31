# Scheme

See schema file through file: Schema.fzz

# Tools

## Access 

* Possible 
    * ssh
* Recommendation 
    * Visual Studio code 

## Run

    python3 lapem.py
    
# Installation
  
## Rasbian

Using the Legacy version without desktop environment
  
## Basic configuration

### SSH

SSH access through

    raspi-config

### Enable Wifi

It is very important to activate the Wifi through raspi-config, specify SSID and Key

You can do it differently, in command line, but you might as well use "raspi-config" for the first time
    
### Update

    sudo apt-get update
    sudo apt-get full-upgrade
  
## Network
 
### Operating mode

Raspberry Pi will work either in Wifi Client mode, or as an Access Point

In order to function as an access point, the Raspberry Pi must have the hostapd access point software package installed

In order to provide network management services (DNS, DHCP) to wireless clients, the Raspberry Pi must have the dnsmasq software package installed

All information at [Raspberry documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point)

    
### Manual Installation

A Raspberry Pi in an Ethernet network, can be used as a wireless access point, creating a secondary network. 

The resulting new wireless network is managed entirely by the Raspberry Pi.

 
#### Wifi

Activate Wifi in file /etc/wpa_supplicant/wpa_supplicant.conf

    ctrl\interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update\config=1
    country=FR
    network={
    ssid="Freebox-CKL-I"
    psk="xxxxxxxxx"
    }

Stop and restart the Wifi

    sudo pkill wpa_supplicant
    sudo wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -B -Dnl80211,wext

#### Access point:

The Raspberry Pi needs to have the hostapd access point software package installed:

    sudo apt-get install hostapd

Create a new configuration file : /etc/hostapd/hostapd.conf

Change : 
* country, 
* ssid , 
* wpa_passphrase : 
to match with yours

**Remark**: wpa_passphrase >8 otherwise the AP does not start

    country_code=FR
    interface=wlan0
    ssid=LapemNetwork
    hw_mode=g
    channel=7
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=secret_password
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP

Verify that configuration file location in /etc/init.d/hostapd containing is there, and if following line is present

    DAEMON_CONF=/etc/hostapd/hostapd.conf

Enable the wireless access point service and set it to start when your Raspberry Pi boots:

    sudo systemctl unmask hostapd
    sudo systemctl enable hostapd
 
#### DHCP Distribution

In order to provide network management services (DNS, DHCP) to wireless clients install dnsmasq

    sudo apt-get install dnsmasq

To configure the distribution DHCP IP range we need to configure /etc/dnsmasq.conf

At the bottom of the file we need to add the following lines.

    interface=wlan0
    dhcp-range=10.3.1450,10.3.14255,12h
    activate the dnsmasq service at boot:

Then

    sudo systemctl enable dnsmasq.service
 
#### AP as static

AP needs to have a static address: configured in etc/dhcpcd.conf

    sudo cp /etc/dhcpcd.conf /etc/dhcpcd-dynamic.conf
    sudo nano /etc/dhcpcd.conf

#Static IP

    interface wlan0
    static ip_address=10.3.141/24
    nohook wpa_supplicant

    sudo cp /etc/dhcpcd.conf /etc/dhcpcd-static.conf

 
#### Default mode AP

Command to run to activate AP for next boot

    sudo systemctl unmask hostapd
    sudo systemctl enable hostapd
    sudo systemctl enable dnsmasq.service

    sudo cp /etc/dhcpcd-static.conf /etc/dhcpcd.conf

 
#### Script to Switch

AP → Client : 
* file : sap2cl.sh

AP → Client
* file : sap2clnsap.sh

Client → AP
* file : sclsap.sh

  
## lapem working directory

    /home/pi/lapem
and
    /home/pi/lapem/music

  
## Samba

[https://raspberry-pi.fr/raspberry-pi-nas-samba/](https://raspberry-pi.fr/raspberry-pi-nas-samba/)

We can now proceed to the installation of Samba :
    sudo apt-get install samba samba-common-bin

I answer Yes to the DHCP question

For safety, make a backup copy of the default Samba configuration file

    sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.org

After that we will edit the configuration file.

    sudo nano /etc/samba/smb.conf

At the end of the file add

    [lapemcode]
        comment= Lapem code 
        path = /home/pi/lapem
        valid users = @users
        force group = users
        create mask = 0660
        directory mask = 0771
        read only = no

    [lapem]
        comment= Lapem music
        path = /home/pi/lapem/music
        valid users = @users
        force group = users
        create mask = 0660
        directory mask = 0771
        read only = no

Close the file by saving it and restart samba

    sudo /etc/init.d/smbd restart

### Samba password

The most important thing is to add a user to samba.
In our example we will add the user pi.

    sudo smbpasswd -a pi
    Password: raspberry

# Connexion Samba

As mentioned we have 2 connection modes

    \\192.168.140\lapem
    \\192.168.140\lapemcode
    \\10.3.141\lapem

    Login : pi
    Password : raspberry

Ubuntu

    smb://192.168.63/lapemcode/

# Program lapem

  
## Help

lapem uses pygame to play music, it must be installed

    sudo apt-get install python-pygame

  
## Other

### Launching at startup

To launch a program at boot time of the Raspberry Pi, you just have to modify the file :/etc/rc.local

In order for the program to be launched, simply add the command line calling your program **exit 0**.

    sleep 3
    /usr/bin/python3 /home/pi/lapem/lapem.py &

The program must give the script back to the program or Raspberry Pi will never finish booting. 
If your program does an infinite loop, you must launch it in the background by adding a & after the command. 
  
## Checking

To verify that the lapem program is running, run the command

    ps -ef | grep lapem