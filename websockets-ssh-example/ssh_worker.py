import paramiko

class SSHWorker(object):
    def __init__(self, host, user, secret, port):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=host, username=user, password=secret,
                            port=port)

        stdin, stdout, stderr = self.client.exec_command('pwd')
        self.path = stdout.read().strip()

    def exec_ls(self):
        stdin, stdout, stderr = self.client.exec_command('ls %s' % self.path)
        return stdout.read().strip().split('\n')

    def exec_cd(self, path):
        if path != '..':
            self.path = ''.join([self.path, '/', path])
        else:
            self.path = self.path[:self.path.rfind('/')]

    def exec_touch(self, name):
        stdin, stdout, stderr = self.client.exec_command('cd %s; touch %s' %
                                                         (self.path, name))

    def exec_cat(self, name):
        stdin, stdout, stderr = self.client.exec_command('cd %s; cat %s' %
                                                         (self.path, name))
        return stdout.read()

    def exec_write(self, name, text):
        stdin, stdout, stderr = self.client.exec_command("cd %s; "
                                                         "echo '%s' > %s" %
                                                         (self.path, text, name))

    def get_filetype(self, name):
        stdin, stdout, stderr = self.client.exec_command('cd %s; '
                                                         'if [ -f "%s" ]; '
                                                         'then echo "1"; fi;'
                                                         % (self.path, name))
        if stdout.read().strip() == '1':
            return 1
        return 0

    def close(self):
        self.client.close()

