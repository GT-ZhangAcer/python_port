# Author:  Acer Zhang
# Datetime:2019/12/15
# Copyright belongs to the author.
# Please indicate the source for reprinting.

# 示例：光照传感器 数据帧 ee cc 02 01 01 00 00 00 00 00 01 00 00 ff有光照


import os
import time
import serial
from serial.tools import list_ports

port_list = list(list_ports.comports())

configs = {"bps": "115200",  # 波特率设置
           "port": "COM3",  # 端口设置
           "time": "1"}  # 超时等待
serial_dict = {'01': "磁检测传感器",
               '02': "光照传感器",
               '0b': "温湿度传感器",
               '0a': "烟雾传感器"}

while True:
    print("----------------------\n当前配置为:", configs)
    opt = input("----------------------\n"
                "1、修改配置\n"
                "2、开始监听\n"
                "3、发送数据\n"
                "4、查看当前端口(虚拟端口可能无法识别)\n"
                "0、退出\n"
                "当前端口数量:" + str(len(port_list)) +
                "\n请输入操作指令_")
    try:
        opt = int(opt)
    except TypeError:
        print("输入有误")
        continue
    if opt == 1:
        print("开始修改配置：\n若无需修改则按回车键跳过")
        new_configs = {}
        for config_item in configs.items():
            config_opt = input(str(config_item) + "\t 新配置_")
            if config_opt is None:
                new_configs[config_item[0]] = config_item[1]
            else:
                new_configs[config_item[0]] = str(config_opt)
    elif opt == 2:
        os.system("cls")
        ser = None
        while True:
            try:
                ser = serial.Serial(port=configs["port"],
                                    baudrate=int(configs["bps"]),
                                    timeout=int(configs["time"]))
                print("监听成功！")
                break
            except Exception as e:
                print("监听失败,堆栈跟踪:\n", e)
                time.sleep(1)
        data = []
        print_index = 0
        frame_index = 0
        while True:
            try:
                one_bit = ser.read(1).hex()  # 此处每次只读1个字节，方便转数据
                data.append(one_bit)
            except:
                print("暂无数据")
                time.sleep(3)
            print_index += 1
            if 'ee' in data and 'cc' in data and 'ff' in data:
                serial_info = data[data.index('cc') + 1]
                this_data = data[data.index('cc') + 4:-1]
                print("第", print_index, "字节|第", frame_index, "帧|原始数据\n", )
                try:
                    print("传感器类型：", serial_dict[serial_info])
                    print("传感器数据", this_data)
                except KeyError:
                    print("该传感器暂未录入,完整数据为:\n" + str(data))
                data = []
                frame_index += 1

    elif opt == 3:
        while True:
            try:
                ser = serial.Serial(port=configs["port"],
                                    baudrate=int(configs["bps"]),
                                    timeout=int(configs["time"]))
                print("连接串口成功！")
                break
            except Exception as e:
                print("连接串口失败,堆栈跟踪:\n", e)
                time.sleep(1)
        while True:
            try:
                send_info = input("请输入字符串_")
                ser.write(send_info.encode("gbk"))
            except Exception as e:
                print("发送失败，堆栈跟踪:\n", e)
    elif opt == 4:
        for i in port_list:
            print(i.description, i.device)
        input("按任意键继续")
    else:
        input("输入有误，请重新输入!\n按任意键重新输入")
    os.system("cls")
