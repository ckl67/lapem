#!/bin/bash
# This script will stop Hotspot (AP+DHCP) and will Switch your Raspberry to a WIFI Client (Definitely) 
# Effect is dynamic and definive --> Next start will be as Client mode
# AND WILL REBOOT
# Run : bash sap2cl.sh

echo "========================================="
echo " Switch from Hotspot (AP+DHP) to Client  "
echo " AND WILL REBOOT !                       "
echo "    Modify your current SSID             "
echo "    ssh to Rasp Client                   "
echo "  Next start will be : Wifi Client mode  "
echo "========================================="
echo " "
echo "Stopping hostapd, dnsmasq "
sudo systemctl stop hostapd.service
sudo systemctl stop dnsmasq.service

echo "Configure Client to recover dhcp"
sudo cp  /etc/dhcpcd-dynamic.conf /etc/dhcpcd.conf
sudo systemctl daemon-reload

echo "Restart wpa_supplicant"
sudo pkill wpa_supplicant
sleep 2
sudo wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -B -Dnl80211,wext

sleep 2
sudo reboot

echo "Done."
exit

