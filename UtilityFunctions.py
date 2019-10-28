import os
from sys import platform
from time import gmtime, strftime

import GlobalVariables as GB


def get_download_path():
    """
    Returns the default downloads path for linux or windows
    (c) Lunar
    """
    if platform == "win32":
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def getIP():
    """
    nothing special just returns IPv4 of this pc (mac is not a pc!)
    (c) Lunar
    """
    import socket

    if platform == "linux" or platform == "linux2":
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    elif platform == "darwin":
        debugOutput(r"""you're running MacOS, i'm not gonna support this thing.""")

    elif platform == "win32":
        return socket.gethostbyname(socket.gethostname())


def convertCode(code, is_hex):
    """
    converts connect code into IP and back
    hex code looks like "XX:XX:XX:XX"
    decimal code looks like ipv4 IP "XXX.XXX.XXX.XXX"
    (c) Lunar
    """
    sepSymbol = ':'
    return '.'.join([str(int('0x' + i, 16)) for i in code.split(sepSymbol)]) \
        if is_hex else sepSymbol.join([hex(int(i)).lstrip('0x') for i in code.split('.')])


def checkAddress(address):
    """
    takes string and returns True if code is correct and False if not
    :param address:
    :return str:
    """
    return convertCode(convertCode(address, is_hex=True), is_hex=False) == address


def fileSize(file_path):
    """
    this function will return the file size
    :param file_path:
    :return str:
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return int(file_info.st_size)


def debugOutput(*args, **kwargs):
    """
    this functions outputs to console what you will give it. output looks like
    DEBUG: Y-m-d H:M:S : your text;
    :param args:
    :param kwargs:
    :return:
    """
    if GB.isDebugEnabled:
        output = ' '.join(str(i) for i in args), ' '.join(str(i) for i in kwargs)
        print('DEBUG: ', strftime("%Y-%m-%d %H:%M:%S", gmtime()), ' : ', *output, ';', sep='')


def setStatus(set_name_func, status):
    set_name_func(GB.WINDOW_NAME + " - " + status)


def sockProtocolConverter(data):
    """
    this thing returns cut off data from received bytes.
    :param data:
    :return str:
    """
    return data.lstrip(r"b\'").rstrip('\'').rstrip(' ')
