#!/bin/bash
echo "Executing Git PULL"
git pull
printf "\n"
echo "Restarting OSINTsploit"
systemctl restart osintsploit.service
printf "\n"
echo "Status : OSINTsploit"
systemctl status osintsploit.service | head
printf "\n"
echo "Restarting NGINX"
systemctl restart nginx.service
printf "\n"
echo "Status : NGINX"
systemctl status nginx.service | head
