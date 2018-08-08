import paramiko


class _LocalFileServer:
    def __init__(self, *args, **kwargs):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def open(self, *args, **kwargs):
        return open(*args, **kwargs)


class FileServer:
    def __new__(cls, hostname=None, username=None, *, port=None):
        if hostname is None:
            return _LocalFileServer()
        else:
            return super().__new__(cls)

    def __init__(self, hostname=None, username=None, *, port=22):
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        self._sftp = None

        self._hostname = hostname
        self._port = port
        self._username = username

    def connect(self):
        self._client.connect(hostname=self._hostname, port=self._port, username=self._username)
        self._sftp = self._client.open_sftp()

    def disconnect(self):
        self._client.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def open(self, *args, **kwargs):
        return self._sftp.file(*args, **kwargs)
