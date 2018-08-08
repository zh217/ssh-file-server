import subprocess

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

    def exec(self, cmd, bytes=False):
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        try:
            if bytes:
                out = res.stdout.splitlines()
            else:
                out = res.stdout.decode('utf-8').splitlines()
        except Exception:
            out = []
        try:
            if bytes:
                err = res.stderr.splitlines()
            else:
                err = res.stderr.decode('utf-8').splitlines()
        except Exception:
            err = []
        return out, err


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

    def exec(self, cmd, bytes=False):
        _, out_f, err_f = self._client.exec_command(cmd)
        try:
            if bytes:
                out = out_f.read().splitlines()
                err = err_f.read().splitlines()
            else:
                out = out_f.read().decode('utf-8').splitlines()
                err = err_f.read().decode('utf-8').splitlines()
        finally:
            out_f.close()
            err_f.close()

        return out, err
