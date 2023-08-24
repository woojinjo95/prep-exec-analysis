sudo iptables -A INPUT -i br0 -j ACCEPT
sudo iptables -A OUTPUT -o br0 -j ACCEPT
sudo iptables -A FORWARD -i br0 -j ACCEPT
sudo iptables -A FORWARD -o br0 -j ACCEPT

sudo iptables -A FORWARD -i enp0s31f6 -o enx00e099008746 -j ACCEPT
sudo iptables -A FORWARD -i enx00e099008746 -o enp0s31f6 -j ACCEPT

sudo ebtables -A FORWARD -i enp0s31f6 -o enx00e099008746 -j ACCEPT
sudo ebtables -A FORWARD -i enx00e099008746 -o enp0s31f6 -j ACCEPT

# sudo iptables -F
# sudo iptables -X
# sudo iptables -t nat -F
# sudo iptables -t nat -X
# sudo iptables -t mangle -F
# sudo iptables -t mangle -X
# sudo iptables -P INPUT ACCEPT
# sudo iptables -P FORWARD ACCEPT
# sudo iptables -P OUTPUT ACCEPT
