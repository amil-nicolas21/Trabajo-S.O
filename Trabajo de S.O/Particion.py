from Proceso import Proceso


class Particion:
    def __init__(self, id: int, tamaño: int):
        self.id = id
        self.tamaño = tamaño
        self.proceso = ''
        self.tamaño_restante = tamaño

    def asignar_part(self, proceso: Proceso):
        proceso.particion = self.id
        self.proceso = proceso
        self.tamaño_restante = self.tamaño_restante - proceso.tamaño
    
    def desasignar_part(self):
        self.tamaño_restante = self.tamaño
        self.proceso = ''


    def vacio(self):
        if (self.proceso == ''):
            return True
        else: 
            return False