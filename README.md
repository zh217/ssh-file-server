# SSH file server

A python package for conveniently access files on SSH.

Requires python 3.5 or above. Install with:

```bash
pip3 install ssh_file_server
```

Example usage:

```python
from ssh_file_server import FileServer

with FileServer('your.ssh.host', 'username') as s:
    with s.open('./a-file', 'r') as file:
        print(file.readlines())
    stdout, stderr = s.exec('ls -lh .')
    for l in stdout:
        print(l)
```

Authentication details (RSA keys, known-hosts) will be read from the current user account.

Works on Windows as well if you have openssh-style .ssh directory setup.

If you just do `FileServer()` without giving any argument, a fake server which accesses local files directly will be returned.