"""
Пути к файлам
"""
import platform

MAIN_WINDOW_UI = 'main_window.ui'
LOGIN_UI = 'LoginWindow.ui'
REGISTRATION_UI = 'RegistrationWindow.ui'

DATA = 'data.csv'

if platform.system() == 'Windows':
    LOGIN_PY = 'main_login.py'
elif platform.system() == 'Linux':
    LOGIN_PY = 'python3 main_login.py'
