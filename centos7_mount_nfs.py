#!/bin/bash

### NFS Mount.sh

################################################
MOUNT_PATH=/nas
NFS_PATH=10.250.53.85:/n2531870_jje
SYSTEMD_PATH=/etc/systemd/system/$(dirname $MOUNT_PATH/aaa).mount
MOUNT=$(basename "$SYSTEMD_PATH")
################################################

mkdir $MOUNT_PATH

yum install -y nfs-utils > /dev/null
echo "Completed Install nfs-utils"

systemctl start rpcbind
systemctl enable rpcbind
chmod 644 /etc/hosts.allow /etc/hosts.deny

# systemd, for Service autostarting
##############################################################
cat << EOF > $SYSTEMD_PATH
[Unit]
Description=Mount NFS data Volume at boot
#Before=httpd.service tomcat.service

[Mount]
What=$NFS_PATH
Where=$MOUNT_PATH
Type=nfs

[Install]
WantedBy=multi-user.target
EOF
##############################################################


systemctl daemon-reload
systemctl enable $MOUNT
systemctl start $MOUNT
df -h
