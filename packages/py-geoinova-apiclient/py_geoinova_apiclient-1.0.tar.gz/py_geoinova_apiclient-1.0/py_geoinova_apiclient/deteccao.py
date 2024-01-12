from .abstract import ApiClientAbstract

class DeteccaoClient(ApiClientAbstract):
    def __init__(self, token, url=None):
        super().__init__(url, token)

    def update_area_ha(self, deteccaoId, areaHa):
        data, ok = self.create_request_post('/deteccoes/area-ha', {'id': deteccaoId, 'areaHa': areaHa})
        if ok:
            return data
        
        return None