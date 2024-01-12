from .abstract import ApiClientAbstract

class AnaliseClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def update_total_area_ha(self, analiseId):
        data, ok = self.create_request_post('/analises/total-area-ha', {'id': analiseId})
        if ok:
            return data
        
        return None

    def update_total_deteccoes(self, analiseId):
        data, ok = self.create_request_post('/analises/total-deteccoes', {'id': analiseId})
        if ok:
            return data
        
        return None

    def get_deteccoes(self, analiseId):
        data, ok = self.create_request_get('/analises/deteccoes/' + str(analiseId))
        if ok:
            return data
        
        return []