import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import socket
import threading
from cryptography.fernet import Fernet

class SecureChat(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        self.server_input = toga.TextInput(placeholder='Адрес сервера (ip:порт)', value='127.0.0.1:5555')
        self.nick_input = toga.TextInput(placeholder='Ваш никнейм')
        self.connect_btn = toga.Button('Подключиться', on_press=self.connect)
        self.status_label = toga.Label('')
        
        main_box.add(self.server_input)
        main_box.add(self.nick_input)
        main_box.add(self.connect_btn)
        main_box.add(self.status_label)
        
        self.main_window.content = main_box
        self.main_window.show()
        
        self.client = None
        self.cipher = None
    
    def connect(self, widget):
        try:
            host, port = self.server_input.value.split(':')
            port = int(port)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
            key = self.client.recv(4096)
            self.cipher = Fernet(key)
            self.client.send(self.nick_input.value.encode())
            self.status_label.text = '✅ Подключено!'
        except Exception as e:
            self.status_label.text = f'❌ Ошибка: {str(e)}'

def main():
    return SecureChat('SecureChat', 'org.securechat')