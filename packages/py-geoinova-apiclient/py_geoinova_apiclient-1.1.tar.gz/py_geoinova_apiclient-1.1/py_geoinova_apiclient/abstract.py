import json
import requests

class ApiClientAbstract:

    def __init__(self, url=None, token=None):
        if url is None:
            url = 'https://api.geoinova.app/v2'
        
        self.url = url
        self.token = token

    def __create_headers(self):
        header = {
            "Content-Type": "application/json"
        }

        if self.token is not None:
            header['Authorization'] = 'Bearer ' + self.token

        return header

    def create_request_get(self, path):
        response = requests.get(self.__resolve_url(path), headers=self.__create_headers())
        protocol, statusCode = self.__process_response(response)
        return self.__process_protocol(protocol, statusCode)
    
    def create_request_post(self, path, data):
        response = requests.post(self.__resolve_url(path), data=json.dumps(data), headers=self.__create_headers())
        protocol, statusCode = self.__process_response(response)
        return self.__process_protocol(protocol, statusCode)

    def create_request_put(self, path, data):
        response = requests.put(self.__resolve_url(path), data=json.dumps(data), headers=self.__create_headers())
        protocol, statusCode = self.__process_response(response)
        return self.__process_protocol(protocol, statusCode)

    def create_request_delete(self, path):
        response = requests.delete(self.__resolve_url(path), headers=self.__create_headers())
        protocol, statusCode = self.__process_response(response)
        return self.__process_protocol(protocol, statusCode)

    def __process_protocol(self, protocol, statusCode):
        if statusCode == 204:
            return {}, True
        
        if len(protocol) == 0:
            return None, False
    
        if protocol['status'] == 'ok':
            return protocol['data'], True
        else:
            return protocol['message'], False

    def __process_response(self, response):
        if response.status_code == 200:
            return response.json(), response.status_code
        elif response.status_code == 201:
            return {}, response.status_code
        elif response.status_code == 204:
            return {}, response.status_code
        else:
            raise Exception(response.text)

    def __resolve_url(self, path):
        return self.url + path