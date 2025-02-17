class Proceso:
    def __init__(self, id:int, tamaño: int, t_arribo: int, t_irrupcion: int):
        self.id = id
        self.tamaño = tamaño
        self.t_arribo = t_arribo
        self.t_irrupcion = t_irrupcion
        self.estado = 'No arribó'
        self.t_restante= t_irrupcion
        self.particion = ''
        self.t_retorno = 0
        self.t_espera = 0
    def nuevo_estado(self, estado: str):
        self.estado= estado

    def restar_tiempo(self):
        if(self.t_restante>0):
            self.t_restante = (self.t_restante - 1)
        else:
            print('Error al restar')

    def termino(self):
        if (self.t_restante == 0) :
            return True
        else: 
            return False
    
    def masretorno(self):
        self.t_retorno = self.t_retorno + 1

