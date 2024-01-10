import threading
import time
import paramiko
from STS.Buffer import CircularBuffer
from STS import logger


class TSSH:
    def __init__(self, host, username, password, port=22, device_name=None, device_type=None, receive_callback=None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.device_name = device_name
        self.device_type = device_type
        self.receive_callback = receive_callback
        self.buffer = CircularBuffer(1024)
        self.ssh = None
        self.ssh_flag = False
        self.curr_context = None
        self.monitor_thread = threading.Thread(target=self.monitor_ssh, daemon=True)

    def login(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, self.port, self.username, self.password)
        self.ssh_flag = True
        self.ssh = client.invoke_shell()
        self.monitor_thread.start()
        self.send_cmd('')

    def logout(self):
        self.ssh_flag = False
        self.monitor_thread.join()
        self.ssh.close()

    def monitor_ssh(self):
        try:

            while self.ssh_flag:
                if self.ssh.recv_ready():
                    recv = self.ssh.recv(1024)
                    self.buffer.append(recv)
                    if self.receive_callback:
                        try:
                            self.receive_callback(recv)
                        except Exception as e:
                            logger.warning(e)
                else:
                    time.sleep(0.1)
        except AttributeError as e:
            logger.error(e)

    def wait_for_string(self, string, timeout=3):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            if self.buffer.find(string):
                return True
            time.sleep(0.1)
        logger.warning(f"Device {self.device_name} Wait For String {string} Timeout")
        return False

    def send_cmd(self, cmd, last_chars=200, delay=0.1):
        if not self.ssh_flag:
            logger.warning(f"Device {self.device_name} Not Opened")
            raise paramiko.SSHException(f"Device {self.device_name} Not Opened")
        try:
            self.ssh.send(f'{cmd}')
            if self.receive_callback:
                self.receive_callback(f'sed:{cmd}'.encode(errors='ignore'))
            time.sleep(delay)
            content = self.buffer.get_contents().decode(encoding='utf-8', errors='ignore')
            return content[-last_chars:]
        except Exception as e:
            logger.exception(str(e))
            raise Exception(e)

    def read_connect(self, length=200):
        connect = self.buffer.get_contents()
        return connect[-length:] if len(connect) > length else connect

    def clear_content(self):
        self.buffer.clear()
