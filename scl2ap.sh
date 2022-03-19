#!/bin/bash
# This script will Switch from Client to Hotspot (AP+DHP) 
# Run : bash scl2ap.sh

echo "========================================="
echo " Switch from Client to Hotspot (AP+DHP)  "
echo " THIS IS NOT DYNAMIC, AND NEEDS A REBOOT "
echo "========================================="
echo " "
echo "Start hostapd, dnsmasq"

sudo systemctl restart dnsmasq.service
sudo systemctl restart hostapd.service

echo "Configure AP wit static IP Address"
sudo cp  /etc/dhcpcd-static.conf /etc/dhcpcd.conf
sudo systemctl daemon-reload

echo "Restart wpa_supplicant"
sudo pkill wpa_supplicant
sleep 2
sudo wpa_supplicant -c/etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -B -Dnl80211,wext

echo "A REBOOT is needed here"
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq.service

sleep 2
sudo reboot

echo "Done."
exit
