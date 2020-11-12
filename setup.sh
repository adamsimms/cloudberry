cur_dir="$( cd "$(dirname "$0")" ; pwd -P )"
user="$(id -u -n)"

sudo sed -i -- "s/^exit 0/su ${user} -c \'screen -mS c -d\'\\nexit 0/g" /etc/rc.local
sudo sed -i -- "s/^exit 0/su ${user} -c \'screen -S c -X stuff \"cd ${cur_dir////\\/}\\\\r\"\'\\nexit 0/g" /etc/rc.local
sudo sed -i -- "s/^exit 0/su ${user} -c \'screen -S c -X stuff \"python main.py\\\\r\"\'\\nexit 0/g" /etc/rc.local
