class ConnError(ConnectionRefusedError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"\n\n!!!警告!!! 请打开<AutoPy Lite>\n\n{self.msg}\n\n"


class PermissionsError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f"\n\n!!!警告!!! 可能没有开启<无障碍>权限;或者没有在App里面开启<开启录屏>选项\n\n"
