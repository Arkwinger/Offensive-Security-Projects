#!/bin/bash

echo "=============================="
echo " Linux Enumeration Script"
echo "=============================="

echo ""
echo "[+] Current User"
whoami

echo ""
echo "[+] Hostname"
hostname

echo ""
echo "[+] Kernel Information"
uname -a

echo ""
echo "[+] Operating System"
cat /etc/os-release

echo ""
echo "[+] IP Addresses"
ip addr show

echo ""
echo "[+] Network Connections"
ss -tulnp

echo ""
echo "[+] Current Directory"
pwd

echo ""
echo "[+] Logged In Users"
who

echo ""
echo "[+] Sudo Permissions"
sudo -l 2>/dev/null

echo ""
echo "[+] Home Directories"
ls /home

echo ""
echo "[+] World Writable Files (first 20)"
find / -type f -perm -002 2>/dev/null | head -20

echo ""
echo "[+] Enumeration Complete"
