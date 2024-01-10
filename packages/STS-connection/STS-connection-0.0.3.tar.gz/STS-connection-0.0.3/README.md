# STS Python库
STS（Serial, Telnet, SSH）是一个用于串口通信、Telnet通信和SSH通信的Python库，提供了Serial、Telnet和SSH等类的实现。

## 安装
使用 pip 安装 STS 库：
`pip install STS-connection`

## Serial 类
Serial 类通过封装 pyserial 库实现了串口通信的二次封装。它包括了一个循环缓冲区、串口监控线程以及打开/关闭串口的方法。

### 示例
```python
from STS.Serial import Serial
serial = Serial('COM3', 115200, 'Serial', 'Serial')
serial.open_port()
resp = serial.send_cmd('hello', delay=1)  # send 'hello' to serial port and wait for 1 second get response
print(resp)
serial.close_port()
```

## Telnet 类
Telnet 类封装了 telnetlib 库，实现了 Telnet 通信。它支持 Telnet 连接、监控数据流、等待指定字符串、发送指令以及读取/清空内容等操作。

### 示例
```python
from STS.Telnet import Telnet
telnet = Telnet(host='example.com', username='your_username', password='your_password', port=23, device_name='MyDevice', device_type='Router')
telnet.login()
resp = telnet.send_cmd('hello', delay=1)  # send 'hello' to telnet and wait for 1 second get response
print(resp)
telnet.logout()
```


## SSH 类
SSH 类使用 paramiko 库实现了 SSH 通信的简单封装。它支持 SSH 连接、监控数据流、等待指定字符串、发送指令以及读取/清空内容等操作。

### 示例
```python
from STS.SSH import SSH
ssh = SSH(host='example.com', username='your_username', password='your_password', port=22, device_name='MyDevice', device_type='Server')
ssh.login()
resp = ssh.send_cmd('hello', delay=1)  # send 'hello' to ssh and wait for 1 second get response
print(resp)
ssh.logout()
```

## 许可
此 Python 库采用 MIT 许可证。