from .abstract import ApiClientAbstract

class AuthClient(ApiClientAbstract):
    def __init__(self, url=None):
        super().__init__(url)

    def signin(self, email, senha):
        data, ok = self.create_request_post('/signin', {'email': email, 'senha': senha, 'manterConectado': False})

        if ok:
            return data['token']
        
        return None