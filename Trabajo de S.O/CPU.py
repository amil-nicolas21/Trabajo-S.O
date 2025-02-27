from Proceso import Proceso

class CPU:
    def __init__(self, quantum = ''):
        self.proceso = ''
        self.quantum= quantum
        self.q_restante = quantum

    def asignar_cpu(self, proceso: Proceso):
        self.proceso = proceso

    def desasignar_cpu(self):
        self.proceso = ''
        if (self.quantum != ''):
            self.q_restante= self.quantum
    
    def procesar(self):
        if (self.proceso == '') :
            print('Error al procesar, CPU vacia')
        else: 
            if (self.quantum != ''):
                if(self.q_restante>0):
                    self.q_restante= self.q_restante-1
                else:
                    print('Error, quantum terminado pero no se desasigno')

    def termino(self):
        if (self.q_restante == 0) :
            return True
        else: 
            return False
    