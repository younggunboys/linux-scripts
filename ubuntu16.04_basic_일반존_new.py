#!/bin/bash

##Ubuntu 16.04##

## Update Package List
apt-get update
#apt install --only-upgrade ��Ű���� #������Ű�� update

## Security Update
apt install -y unattended-upgrades
unattended-upgrade


## Install utils
apt install -y nmap telnet tree wget curl net-tools


## Set Hostname /etc/hosts
echo "127.0.0.1 $(hostname)" >> /etc/hosts

HOSTNAME="$HOSTNAME"
sed -i "s|127.0.0.1       localhost|127.0.0.1       localhost  $HOSTNAME|" /etc/hosts


## Set Accounts

########## Client Account ############
#USER1=xx
#PW1='xx'

#useradd -m -s /bin/bash $USER1

#echo "$USER1    ALL=(ALL)    NOPASSWD: ALL" >> /etc/sudoers
#echo "$USER1:$PW1" | chpasswd




########## SICC Account #############
USER2=sicc
PW2='Mgmt4340!@#'

useradd -m -s /bin/bash $USER2

echo "$USER2    ALL=(ALL)    NOPASSWD: ALL" >> /etc/sudoers
echo "$USER2:$PW2" | chpasswd



# Set Session Timeout
sed -i 's|TMOUT=324000|TMOUT=600|' /etc/profile
echo "export TMOUT" >> /etc/profile
source /etc/profile


# Deny ROOT Login
sed -i 's|PermitRootLogin yes|#PermitRootLogin yes|' /etc/ssh/sshd_config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
systemctl restart sshd


# Set password rule �ҹ���+����+Ư������, ��� 5ȸ �Է� ���� �� 5�а� ���� ���, �빮��(ucredit=-1)

echo "password    requisite     pam_cracklib.so try_first_pass retry=3 minlen=8 lcredit=-1 dcredit=-1 ocredit=-1" >> /etc/pam.d/common-password
echo "account required pam_tally2.so" >> /etc/pam.d/common-account
echo "auth required pam_tally2.so file=/var/log/tallylog deny=5 even_deny_root unlock_time=300" >> /etc/pam.d/common-auth


# Set Password Maximum number of days between password change
#sed -i 's|PASS_MAX_DAYS   99999|PASS_MAX_DAYS   90|' /etc/login.defs
#sed -i 's|PASS_MIN_DAYS   0|PASS_MIN_DAYS   1|' /etc/login.defs



####################
BASHRC=/home/$USER2/.bashrc
####################
#=====================================================
cat << EOF >> $BASHRC 
# Set Prompt Color
#export PS1="\[$(tput bold)$(tput setaf 6)\][\u@\h \[$(tput bold)$(tput setaf 3)\]\W]\\$ \[$(tput sgr0)\]" #cyan, yellow
export PS1="\[$(tput bold)$(tput setaf 6)\][\u@\[$(tput bold)$(tput setaf 3)\]\h \[$(tput bold)$(tput setaf 1)\]\W]\\$ \[$(tput sgr0)\]" #cyan, yellow, red

# Set Alias
alias sdr='sudo systemctl daemon-reload'
alias s='sudo systemctl'
alias nt='sudo netstat -tnlp'
alias lr='ls -lrt'
alias psg='sudo ps -ef | grep'
alias vi=/usr/bin/vim
alias jx='sudo journalctl -xe --no-pager | less | grep'
alias sudo='sudo '
EOF
#=====================================================





# Set vi editor 
###########################
VIMRC=/home/sicc/.vimrc
###########################
cat << EOF >> $VIMRC
"���ȣǥ��
set nu
"�ּ� ���� ����
highlight Comment ctermfg=Cyan
"�˻��ܾ� ���� ����
hi Search term=standout ctermfg=0 ctermbg=3
"�˻��ܾ� ���� ǥ�� on
set hlsearch
"Tab �Է½� 4ĭ �鿩���� �Է�
set tabstop=4
"�͹̳� �ϴ� ���μ�/Ŀ����ġ ǥ��
set ruler
"Ŀ�� ��ġ�� �࿡ ����
set cursorline
"��ҹ��� ���о��� �˻�
set ignorecase
EOF
#####################################################################




# Set changing base editor (nano --> vim)
#update-alternatives --config editor �Է� �� 3�Է�

# Set Login Success Message
#=====================================================
cat << EOF >> /etc/profile.d/motd.sh

        		 ____ 
              __/ \--\ 
              U |_|__|    This is $HOSTNAME Server.
                   || 
   ,   ,   ,   ,   ,|  ,   ,   ,   ,   , 
  ||__||__||__||__|||_||__||__||__||__|| 
  |.--..--..--..--..--..--..--..--..--.| 
  ||  ||  ||  ||  ||| ||  ||  ||  ||  || 
 \\//|\//||/\||/|\/\||\\|//\|\|//\|//\\///

EOF
#=====================================================
				

