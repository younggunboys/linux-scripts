#!/bin/bash
set -e

yum install epel-release -y > /dev/null
yum install -y yum-security tree nmap > /dev/null
yum update --security -y > /dev/null
echo "#Completed yum Security update & Install epel-release, Packages"



# Deny ROOT Login
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
systemctl restart sshd
echo "#Completed RootLogin denying setting"




# Set vi editor 
#################################################
VIMRC=/etc/vimrc
#################################################
cat << EOF >> $VIMRC
"행번호표시
set nu
"주석 색상 설정
highlight Comment ctermfg=Cyan
"검색단어 색상 설정
highlight Search term=standout ctermfg=0 ctermbg=3
"검색단어 색상 표시 on
set hlsearch
"Tab 입력시 4칸 들여쓰기 입력
set tabstop=4
"터미널 하단 라인수/커서위치 표시
set ruler
"커서 위치한 행에 밑줄
set cursorline
"대소문자 구분없이 검색
set ignorecase
"상태바 항상 표시
set laststatus=2
EOF
#################################################
source /etc/bashrc
echo "#Completed Prompt Color, Alias, Vimrc setting"


## Set Accounts : useradd, chpasswd, add sudoers
###########################
#USER1=고객id
#PW1='xx'
###########################
#useradd -m $USER1 && echo '$USER1:$PW1' | chpasswd
#echo "$USER2   ALL=(ALL)    NOPASSWD: ALL" >> /etc/sudoers


###########################
USER2=sicc
PW2='mgmt4340!@#'
###########################
useradd -m $USER2 && echo "$USER2:$PW2" | chpasswd
echo "$USER2   ALL=(ALL)    NOPASSWD: ALL" >> /etc/sudoers
echo "#Completed Accounts setting"


# Create Symbolic Link for systemd  
ln -s /etc/systemd/system/ /systemd


# Set password rule 소문자, 숫자, 특수문자
echo " " >> /etc/security/pwquality.conf
echo "lcredit=-1" >> /etc/security/pwquality.conf
echo "dcredit=-1" >> /etc/security/pwquality.conf
echo "ocredit=-1" >> /etc/security/pwquality.conf
echo "minlen=8" >> /etc/security/pwquality.conf
echo "retry=5" >> /etc/security/pwquality.conf


#sed -i 's|120|90|' /etc/login.defs
sed -i 's|30|7|' /etc/login.defs
echo "#Completed Password Rule setting"


# Set Session Timeout
sed -i 's|TMOUT=324000|TMOUT=600|' /etc/profile
echo "export TMOUT" >> /etc/profile
echo "" >> /etc/profile
source /etc/profile
echo "#Completed Sesstion timeout setting"

####################
BASHRC=/home/$USER2/.bashrc
####################
#=====================================================
cat << EOF >> $BASHRC 
# Set Prompt Color
#export PS1="\[$(tput bold)$(tput setaf 6)\][\u@\h \[$(tput bold)$(tput setaf 3)\]\W]\\$ \[$(tput sgr0)\]" #cyan, yellow
export PS1="\[$(tput bold)$(tput setaf 6)\][\u@\[$(tput bold)$(tput setaf 3)\]\h \[$(tput bold)$(tput setaf 1)\]\W]\\$ \[$(tput sgr0)\]" #cyan, yellow, red

# Set Alias
alias sdr='systemctl daemon-reload'
alias s='systemctl'
alias nt='netstat -tnlp'
alias lr='ls -lrt'
alias psg='ps -ef | grep'
alias vi=/usr/bin/vim
alias jx='journalctl -xe --no-pager | less | grep'
alias sudo='sudo '
EOF
#=====================================================


# Set keeping Log for 6 month
######################################
LOGROTATE=/etc/logrotate.conf
mv $LOGROTATE $LOGROTATE"_bak"
######################################
#=====================================================
cat << EOF >> $LOGROTATE
# see "man logrotate" for details
# rotate log files monthly
monthly

# use the syslog group by default, since this is the owning group
# of /var/log/syslog.
su root syslog

# keep 6 months worth of backlogs
rotate 6

# create new (empty) log files after rotating old ones
create

# uncomment this if you want your log files compressed
#compress

# packages drop log rotation information into this directory
include /etc/logrotate.d

# no packages own wtmp, or btmp -- we'll rotate them here
/var/log/wtmp {
    missingok
    monthly
    create 0664 root utmp
    rotate 6
    dateext
}

/var/log/btmp {
    missingok
    monthly
    create 0660 root utmp
    rotate 6
    dateext
}

# system-specific logs may be configured here
/var/log/umtp {
   monthly
   create 0640 root utmp
   rotate 6
   missingok
   dateext
}
EOF
#=====================================================
echo "#Completed logrotate.conf setting"