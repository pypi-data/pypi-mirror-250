from .abstract import ApiClientAbstract

class CamadaClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def get_camadas_by_ativo_id(self, ativoId):
        data, ok = self.create_request_get('/camadas/' + str(ativoId) + '?:fields=wkt')

        if ok:
            return data
        
        return []