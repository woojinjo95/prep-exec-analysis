sudo apt install -y apt-transport-https 
sudo apt install -y ffmpeg
sudo apt install -y v4l-utils
sudo apt install -y ubuntu-restricted-extras
sudo apt install -y libavcodec58
sudo apt install -y cpufrequtils
sudo apt install -y ifmetric
sudo apt install -y dkms
sudo apt install -y alsa-utils

# for wifi connectio in server
sudo apt install -y wireless-tools wpasupplicant

# Docker
sudo apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
docker -v 
sudo systemctl enable docker && service docker start  # PW 입력


# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


# cpu setting
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl disable ondemand


# magewell capture board
wget https://www.magewell.com/files/drivers/ProCaptureForLinux_4328.tar.gz 
tar xvzf ProCaptureForLinux_4328.tar.gz
cd ProCaptureForLinux_4328
sh install.sh

# alsa mixer default 
amixer -c 1 set Capture 90% 

# permission serial & video
sudo usermod -a -G dialout $USER
sudo usermod -a -G video $USER

# docker permission
sudo chmod 666 /var/run/docker.sock
sudo groupadd --force docker
sudo usermod -aG docker $USER
newgrp docker

# login service
mkdir -p $HOME/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCzh/nSonLYGS/iinpY4TGB3LoETtrHWOv4est/iS+TMmmnllQ/25zB+96PdZMI0hTbcbq40WJbz1CkFcfySsvsF8Sv9vzLSAhXEPnIXdkUnPr3VAQmWAWSUfQlTfXhviU3+QcAFr1GOOq9YheYJG/5XVEgVaPIk9jvsdSRUy8IGWzOFI/JyB+zFr3pUsD+jx3ShFF8goDS9zLjhUGCCQjiXRhoMdsb4Nh5EdKI2Psr1t1A+5uREO0+8hBUkyy0MD1lm+xS8A5Wp8iAn33O1FUZvC38Pe2Q+ZPKvcwMKzysXaV2V/hGKfIQ0VNO+wK0kGAz0ICZ+27/o6tN1brV7sWH5u0pAYdsPFaghl6YOMjNwKH5lrjXQt2HQozu51adIekuyNHWOMGAT7hua/V8AJHA6TzhJ0eyF5itDuP6wNYgv/12x5K2ogdRwln3RxtPx3FbrtgEYqiAiGX7522IpdwTYHFyB05cC6+ij3YlnlSIVYeJwD8Mg2JFRpvfFz7cd3s=" > $HOME/.ssh/authorized_keys
chmod 600 $HOME/.ssh/authorized_keys