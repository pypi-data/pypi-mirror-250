import threading
import time
import telnetlib
from STS.Buffer import CircularBuffer
from STS import logger


class TTelnet:
    def __init__(self, host, port=23, device_name=None, device_type=None, receive_callback=None):
        self.host = host
        self.port = port
        self.device_name = device_name
        self.device_type = device_type
        self.receive_callback = receive_callback
        self.buffer = CircularBuffer(1024)
        self.telnet = None
        self.telnet_flag = False
        self.curr_context = None
        self.monitor_thread = threading.Thread(target=self.monitor_telnet, daemon=True)

    def login(self, username, password):
        self.telnet = telnetlib.Telnet(self.host, self.port)
        self.telnet_flag = True
        self.monitor_thread.start()
        self.send_cmd('')
        self.send_cmd(username)
        self.send_cmd(password)

    def logout(self):
        self.telnet_flag = False
        self.monitor_thread.join()
        self.telnet.close()

    def monitor_telnet(self):
        try:
            while self.telnet_flag:
                if self.telnet.sock_avail():
                    recv = self.telnet.read_eager()
                    self.buffer.append(recv)
                    if self.receive_callback:
                        try:
                            self.receive_callback(recv)
                        except Exception as e:
                            logger.warning(e)
                else:
                    time.sleep(0.1)
        except Exception as e:
            logger.error(e)

    def wait_for_string(self, string, timeout=3):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            if self.buffer.find(string):
                return True
            time.sleep(0.1)
        logger.warning(f"Device {self.device_name} Wait For String {string} Timeout")
        return False

    def send_cmd(self, cmd, last_chars=200, delay=0.2):
        if not self.telnet_flag:
            logger.warning(f"Device {self.device_name} Not Opened")
            raise Exception(f"Device {self.device_name} Not Opened")
        try:
            self.telnet.write(f'{cmd}'.encode())
            if self.receive_callback:
                self.receive_callback(f'sent:{cmd}'.encode(errors='ignore'))
            time.sleep(delay)
            content = self.buffer.get_contents().decode(encoding='utf-8', errors='ignore')
            return content[-last_chars:]
        except Exception as e:
            logger.exception(str(e))
            raise Exception(e)

    def read_content(self, length=200):
        content = self.buffer.get_contents()
        return content[-length:] if len(content) > length else content

    def clear_content(self):
        self.buffer.clear()


