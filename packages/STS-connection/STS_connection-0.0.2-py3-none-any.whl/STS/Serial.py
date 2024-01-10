import logging
import threading
import time

import serial
from STS.Buffer import CircularBuffer
from STS import logger


class Serial:
    def __init__(self, serial_port, baud_rate, device_name, device_type, receive_callback=None, debug=False):
        '''
        二次封装了pyserial，增加了缓冲区和串口监控线程
        :param serial_port: 端口号
        :param baud_rate: 波特率
        :param device_name: 设备名称
        :param device_type: 设备类型
        '''
        self.ser_flag = False
        self.curr_context = None
        self.receive_callback = receive_callback
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.device_name = device_name
        self.device_type = device_type
        self.buffer = CircularBuffer(1024)
        self.monitor_thread = threading.Thread(target=self.monitor_serial)
        self.monitor_thread.daemon = True  # 设置为守护线程，主线程结束时会自动退出
        # self.lock = threading.Lock() #此处如果加锁，会导致串口监控线程阻塞，速度太慢
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)

        logger.debug(f"Device {self.device_name} Created: {self.serial_port}, {self.baud_rate}, {self.device_type}")

    def open_port(self):
        '''
        打开串口
        :return: 返回串口打开结果
        '''
        self.ser_flag = True
        self.monitor_thread.start()
        if self.ser.is_open:
            return True
        else:
            self.ser.open()
            if self.ser.is_open:
                logger.debug(f"Device {self.device_name} Opened")
                return True
            else:
                logger.error(f"Device {self.device_name} Open Failed")
                return False

    def close_port(self):
        '''
        关闭串口
        :return: fanhui 串口关闭结果
        '''
        self.ser_flag = False
        if self.serial_port and self.ser.is_open:
            self.monitor_thread.join()
            self.ser.close()
            self.serial_port = None
            if not self.ser.is_open:
                logger.debug(f"Device {self.device_name} Closed")
                return True
            else:
                logger.error(f"Device {self.device_name} Close Failed")
                return False
        else:
            logger.warning(f"Device {self.device_name} Not Opened")
            return True

    def monitor_serial(self):
        '''
        串口监控线程，将串口数据读取到缓冲区
        :return:
        '''
        while self.ser.is_open and self.ser_flag:
            try:
                # while self.ser.in_waiting:  # 这个判断原来是用来判断串口是否有数据要接受，但是判断速度太慢，会导致串口监控线程阻塞
                # logger.debug(f'serial out waiting:{self.ser.out_waiting}')
                self.curr_context = self.ser.read_until()
                logger.debug(self.curr_context.decode(errors='ignore')[:-1])
                # with self.lock:
                self.buffer.append(self.curr_context)
                if self.receive_callback:
                    try:
                        self.receive_callback('rec:' + self.curr_context.decode(errors='ignore'))
                    except Exception as e:
                        logger.warning(e)
                # else:
                #     time.sleep(0.1)
            except AttributeError as e:
                logger.warning(e)
                pass

    def wait_for_string(self, string, timeout=3):
        '''
        等待串口接收到指定字符串
        :param string: 等待的字符串
        :param timeout: 等待超时时间
        :return: 等待结果
        '''
        start_time = time.time()
        while True:
            # print(self.curr_context)
            if time.time() - start_time > timeout:
                logger.warning(f"Device {self.device_name} Wait For String {string} Timeout")
                return False
                # with self.lock:
            elif self.buffer.find(string):
                return True
            else:
                time.sleep(0.01)

    def send_cmd(self, cmd, last_chars=200, delay=0.1):
        '''
        发送指令到串口 并等待串口返回指定长度的字符串
        :param cmd: 要发送的指令
        :param last_chars: 返回的字符串长度
        :param delay: 发送完成后等待回显的时间
        :return: 发送完成后的回显
        '''
        if self.ser:
            try:
                self.ser.write(cmd.encode())
                if self.receive_callback:
                    self.receive_callback('sed:' + cmd)
                # with self.lock:
                time.sleep(delay)
                content = self.buffer.get_contents().decode(encoding='utf-8', errors='ignore')
                return content[-last_chars:]
            except Exception as e:
                logger.exception(str(e))
                raise Exception(e)
        else:
            logger.error(f"Device {self.device_name} Not Opened")
            raise serial.SerialException("Serial Port Not Opened")

    def read_content(self, length=200):
        '''
        读取串口缓冲区的内容
        :return: 串口缓冲区内容
        '''
        # with self.lock:
        content = self.buffer.get_contents()
        if len(content) > length:
            connect = content[-length:]

        return content.decode(encoding='utf-8', errors='ignore')

    def clear_content(self):
        self.buffer.clear()
