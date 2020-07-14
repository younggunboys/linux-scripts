## 디스크 1개 추가하는 경우, fdisk /dev/xvdb 실행 이후 작업들


#!/bin/bash
set -e

################################################
MOUNT_PATH=/data
DEVICE=/dev/xvdb1
TYPE=xfs
################################################

echo "==============================="
mkfs.$TYPE $DEVICE
echo "==============================="
fsck -y $DEVICE
echo ""
echo "==============================="

mkdir $MOUNT_PATH
cp /etc/fstab /etc/fstab.bak

blkid $DEVICE > uuid.txt
UUID=`cut -f 2 -d '"' uuid.txt`

#===================================================
cat << EOF >> /etc/fstab
UUID=$UUID $MOUNT_PATH           $TYPE    defaults,nofail              0       0
EOF
#===================================================

mount -a

df -h
