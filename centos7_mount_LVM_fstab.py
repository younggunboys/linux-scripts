## 디스크 1개 LVM 설정하는 경우, fdisk /dev/xvdb 실행 이후 작업들
## 부팅 시 자동 마운트 설정 포함


#!/bin/bash
set -e

################################################
MOUNT_PATH=/data
PV=/dev/xvdb1
VG=vg
LV=lv
TYPE=xfs
################################################

yum -y install lvm2
pvcreate $PV
vgcreate $VG $PV
lvcreate --extents +100%FREE -n $LV $VG

echo "==============================="
mkfs.$TYPE /dev/$VG/$LV
echo "==============================="
fsck -y /dev/$VG/$LV
echo ""
echo "==============================="

mkdir $MOUNT_PATH
cp /etc/fstab /etc/fstab.bak

#===================================================
cat << EOF >> /etc/fstab
/dev/mapper/$VG-$LV   $MOUNT_PATH         $TYPE    defaults,nofail              0       0
EOF
#===================================================

mount -a
df -h

