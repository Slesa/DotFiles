```
echo "hw.syscons.bell=0" >> /etc/sysctl.conf
sudo sysctl kern.vt.enable_bell=0
echo "kern.vt.enable_bell=0" >> /etc/sysctl.conf
```

Intel Graphic:
```
sysrc -f /etc/rc.conf kld_list+=i915kms
```

/etc/rc.conf
```
clear_tmp_enable="YES"
syslogd_flags="-ss"
sendmail_enable="NONE"
linux_enable="YES"
hostname="stibbons"
ifconfig_wlan0="WPA DHCP"
sshd_enable="YES"
ntpd_enable=YES
ntpd_sync_on_start=YES
powerd_enable="YES"
dbus_enable="YES"
hald_enable="YES"
slim_enable="YES"
# Set dumpdev to "AUTO" to enable crash dumps, "NO" to disable
dumpdev="AUTO"
zfs_enable="YES"
kld_list="i915kms"

wpa_supplicant_conf_file="/etc/wpa_supplicant.conf"
ifconfig_wlan0="WPA DHCP"
wlans_iwn0="wlan0"
```
