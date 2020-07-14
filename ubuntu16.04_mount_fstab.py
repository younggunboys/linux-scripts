## 디스크 1개 추가하는 경우, fdisk /dev/xvdb 실행 이후 작업들


#!/bin/bash
set -e

################################################
MOUNT_PATH=/tree
DEVICE=/dev/xvdb1
TYPE=ext4
################################################

echo "=================="
mkfs.$TYPE $DEVICE
echo "=================="
echo ""
echo ""
echo "=================="
fsck -y $DEVICE
echo "=================="



mkdir $MOUNT_PATH
cp /etc/fstab /etc/fstab.bak

blkid $DEVICE > uuid.txt
UUID=`cut -f 2 -d '"' uuid.txt`
echo ""
echo ""
#===================================================
cat << EOF >> /etc/fstab
UUID=$UUID $MOUNT_PATH           $TYPE    defaults,nofail              0       0
EOF
#===================================================


mount -t $TYPE $DEVICE $MOUNT_PATH

df -h
