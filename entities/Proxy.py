class Proxy:
    proxy_type = None
    ip = None
    port = None
    login = None
    password = None

    def __init__(self, proxy_type, ip, port, login, password):
        self.proxy_type = proxy_type
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    def __str__(self):
        return f'{self.proxy_type}://{self.login}:{self.password}@{self.ip}:{self.port}'