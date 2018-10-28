import Enlace as enl

class PacoteIP:
    def __init__(self, source='192.168', destination='192.168', mask='255.0'):
        self.source = source # endereço a ser atribuido como próprio
        self.destination = destination
        self.mask = mask
        self.data = ''

class CamadaRede:
    def __init__(self, address='0.0', mask='255.0'):
        self.enlace = enl.CamadaEnlace() # Camada física
        self.address = address # endereço a ser atribuido como próprio
        self.mask = mask



