from .abstract import ApiClientAbstract

class DeteccaoCamadaClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def insert_deteccao_camada(self, deteccaoId, camadaId):
        return self.create_request_post('/deteccoes/camadas', {'deteccaoId': deteccaoId, 'camadaId': camadaId})