# set usb devices
usb_bt=/dev/ttyUSB0
usb_ir=/dev/ttyUSB1

# check_device() {
# # 시리얼 장치에 테스트 데이터 송신하여 장치 종류가 IR인지 BT인지 식별
# # args: [장치 이름, 테스트 커맨드, BAUDRATE]
# # ret:  1이면 BT. 0이면 제어보드
#   exec 3<>$1                              # 3번 fd(file descriptor)에 장치 할당
#   stty -F $1 $3 cs8 -cstopb -parenb       # set baudrate
#   echo "send data to $1"
#   echo $2 >&3                             # send test data
#   sleep 1

#   timeout 2s cat <&3 > tmp.txt            # write data to file from fd and kill `cat` process
#   RET=$(cat tmp.txt)                      # read data from tmp file
#   rm tmp.txt

#   COMMAND="${COMMAND:0:${#COMMAND}}"
#   RET="${RET:0:${#COMMAND}}"                       # post-process for invalid string
#   echo "command: $COMMAND / length: ${#COMMAND}"
#   echo "return: $RET  / length: ${#RET}"

#   # compare return value
#   if [ "$RET" = "Waiting 5 seconds..." ]; then
#     echo "data is returned"
#     return 1
#   else
#     echo "datas is not returned"
#     return 0
#   fi
# }

# Get Product ID and Vendor ID of usb devives 
id_output=$(lsusb)
cp210x_id=$(echo "$id_output" | grep "CP210x UART Bridge" | awk '{print $6}')

echo "cp210_id: $cp210x_id"

IFS=":" read -ra parts <<< "$cp210x_id"

vendor_id="${parts[0]}"
product_id="${parts[1]}"

echo "vendor_id: $vendor_id" && echo "product_id: $product_id"

usb_bt_serial=$(udevadm info -a -n $usb_bt | grep '{serial}' | head -n1 | sed -n 's/.*"\(.*\)"/\1/p')
usb_ir_serial=$(udevadm info -a -n $usb_ir | grep '{serial}' | head -n1 | sed -n 's/.*"\(.*\)"/\1/p')


echo "usb_bt_serial: $usb_bt_serial" && echo "usb_ir_serial: $usb_ir_serial"

# confirm usb file
udev_rule_file_path="/etc/udev/rules.d/99-usb-serial.rules"

if [ -e "$udev_rule_file_path" ]; then
    confirm_file=1
    echo "usb serial set 파일이 존재합니다."
else
    confirm_file=0
    echo "usb serial set 존재하지 않습니다."
fi

# mapping sysmbol link & grant access
if [ $confirm_file = 1 ]; then
    if grep -q "MODE=\"0666\"" "$udev_rule_file_path"; then
        echo "usb sysmbol link 및 접근권한이 존재하기에 작업을 종료합니다."
    else
        new_rule_bt="SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$vendor_id\", ATTRS{idProduct}==\"$product_id\", ATTRS{serial}==\"$usb_bt_serial\", MODE=\"0666\", SYMLINK+=\"ttyBT\""
        new_rule_ir="SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$vendor_id\", ATTRS{idProduct}==\"$product_id\", ATTRS{serial}==\"$usb_ir_serial\", MODE=\"0666\", SYMLINK+=\"ttyCB\""
        new_rules="$new_rule_bt\n$new_rule_ir"
        echo -e "$new_rules" > $udev_rule_file_path
        echo "접근권한을 추가하였으며 작업을 종료합니다."
    fi
else
    RULE_FILE_PATH=/etc/udev/rules.d/99-usb-serial.rules
    rm $RULE_FILE_PATH
    RULE_FILE_CONTENT1="SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$vendor_id\", ATTRS{idProduct}==\"$product_id\", ATTRS{serial}==\"$usb_bt_serial\", MODE=\"0666\", SYMLINK+=\"ttyBT\""
    RULE_FILE_CONTENT2="SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"$vendor_id\", ATTRS{idProduct}==\"$product_id\", ATTRS{serial}==\"$usb_ir_serial\", MODE=\"0666\", SYMLINK+=\"ttyCB\""
    RULE_FILE_CONTENT="$RULE_FILE_CONTENT1\n$RULE_FILE_CONTENT2"
    echo -e $RULE_FILE_CONTENT >> $RULE_FILE_PATH
    echo "write rule to file => $RULE_FILE_PATH"
    echo "file content:  $(cat $RULE_FILE_PATH)"

    sudo service udev reload
    sudo service udev restart

    echo "usb sysbom link 작업을 완료했습니다."
fi

echo "작업 내용 적용을 위해 시스템을 재시작합니다."
sudo reboot