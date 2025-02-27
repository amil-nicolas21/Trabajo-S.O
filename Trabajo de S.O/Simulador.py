from Proceso import Proceso
from Particion import Particion
from CPU import CPU
from collections import namedtuple

Cpu = namedtuple('Cpu', ['id', 't_restante'])
Reg = namedtuple("Reg", ["listaNoAdmitidos", "listaNuevos", "listaListos", "listaTerminados", "CC", "cpu"])

number = ['1','2','3','4','5','6','7','8', '9', '0']

class Simulador: 
    def __init__(self, tecnica, seleccion_part, tamaño_so, multiprogramacion, quantum = ''):
        self.seleccion_part = seleccion_part
        self.tecnica = tecnica
        self.multiprogramacion = multiprogramacion
        self.quantum= quantum
        self.listaNuevos = []
        self.listaListos = []
        self.listaTerminados = []
        self.listaNoAdmitidos = []
        self.particiones = [Particion(0, tamaño_so)]
        self.cpu = None
        self.tiempo = 0
        self.tiempo_actual = 0
        self.arregloTiempos= []
        self.iniciales = 0
        self.tiempoRetornoProm= 0
        self.tiempoEsperaProm = 0
        self.rendimiento = 0
        self.pararxContexto = False
    

    def abrirArchivo(self, direccion: str):
        with open(direccion) as archivo:
            for line in archivo:
                if(line[0] in number):
                    x= 0
                    id = ''
                    tam = ''
                    t_arribo = ''
                    t_irr= ''
                    while line[x] != ';':
                        id = id +line[x]
                        x = x +1
                    x = x+1
                    while line[x] != ';':
                        tam = tam +line[x]
                        x = x +1
                    x = x +1
                    while line[x] != ';':
                        t_arribo = t_arribo +line[x]
                        x = x +1
                    x = x +1
                    while line[x] != ';':
                        t_irr = t_irr +line[x]
                        x = x +1
                    self.agregarNoAdmitido(Proceso(int(id), int(tam), int(t_arribo), int(t_irr)))
                    self.iniciales = self.iniciales + 1
            
                    
    
    def verificarAdmitidos(self):
        if (self.listaNoAdmitidos != 0):
                eliminados=[]
                for x in range(0, len(self.listaNoAdmitidos)):
                    if (self.listaNoAdmitidos[x].t_arribo <= self.tiempo):
                        if(len(self.listaNuevos) + len(self.listaListos) < self.multiprogramacion):
                            self.agregarNuevo(self.listaNoAdmitidos[x])
                            eliminados.append(self.listaNoAdmitidos[x].id)
                for i in range(0, len(eliminados)):
                    self.eliminarNoAdmitido(eliminados[i])

                    

    def crearParticion(self, particion: Particion):
        self.particiones.append(particion)

    def eliminarParticion(self, index: int):
        if (index == 0):
            print('No puede eliminarse el S.O.')
        del self.particiones[index]


    def agregarNoAdmitido(self, proceso: Proceso):
        self.listaNoAdmitidos.append(proceso)

    def eliminarNoAdmitido(self, id: int):
        x= 0
        while (x<=len(self.listaNoAdmitidos)):
            if (self.listaNoAdmitidos[x].id == id):
                del self.listaNoAdmitidos[x]
                return
            else:
                x= x +1

    def agregarNuevo(self, proceso: Proceso):
        self.listaNuevos.append(proceso)

    def eliminarNuevo(self, id: int):
        x= 0
        while (x<=len(self.listaNuevos)):
            if (self.listaNuevos[x].id == id):
                del self.listaNuevos[x]
                return
            else:
                x= x +1

    
    def agregarListo(self, proceso: Proceso):
        self.listaListos.append(proceso)
        

    def eliminarListo(self, id: int):
        x= 0
        while (x<=len(self.listaListos)):
            if (self.listaListos[x].id == id):
                del self.listaListos[x]
                return
            else:
                x= x +1
    
    def desasignar_particion(self,id:int):
        x=0
        while (x<=len(self.particiones)):
            if (self.particiones[x].id == id):
                self.particiones[x].desasignar_part()
                self.particiones[x].proceso = ''
                return
            else:
                x = x+1

    def Promedios(self):
        for i in range(0, len(self.listaTerminados)):
            self.tiempoRetornoProm = self.listaTerminados[i].t_retorno + self.tiempoRetornoProm
            self.tiempoEsperaProm = self.listaTerminados[i].t_espera + self.tiempoEsperaProm
        
        self.tiempoRetornoProm = (self.tiempoRetornoProm)/ len(self.listaTerminados)
        self.tiempoEsperaProm = (self.tiempoEsperaProm)/ len(self.listaTerminados)
        
    def calcularRendimiento(self):
        self.rendimiento = len(self.listaTerminados)/self.tiempo

    def agregarTerminado(self, proceso: Proceso):
        proceso.t_espera = proceso.t_retorno - proceso.t_irrupcion
        self.listaTerminados.append(proceso)
        if(self.iniciales == len(self.listaTerminados)):
            self.Promedios()
            self.calcularRendimiento()

    def eliminarTerminado(self, id: int):
        x= 0
        while (x<=len(self.listaTerminados)):
            if (self.listaTerminados[x].id == id):
                del self.listaTerminados[x]
                return
            else:
                x= x +1


            
    def crearCpu(self):
        if (self.tecnica == 'R.R'):
            self.cpu = CPU(int(self.quantum))
        else: 
            if(self.tecnica == 'SJF'):
                self.cpu = CPU()
            else: 
                print('Método no implementado. No se puede crear CPU')
    
    def eliminarCpu(self):
        self.cpu = None

    
    def buscarParticion(self, tam): 
        if(self.seleccion_part == 'W.F'):
            indice = 0
            max = 0
            for i in range (1, len(self.particiones)):
                if (self.particiones[i].vacio()) and (self.particiones[i].tamaño > max):
                    indice = i
                    max = self.particiones[i].tamaño
            return indice
        else:
            if(self.seleccion_part == 'B.F'):
                indice = 0
                min = 1000000
                for i in range (1, len(self.particiones)):
                    if (self.particiones[i].vacio()) and (self.particiones[i].tamaño>=tam ) and ((self.particiones[i].tamaño - tam) < min):
                        indice = i
                        min = self.particiones[i].tamaño - tam
                return indice 
            else:
                print('Tecnica no implementada')

    def agregartiempos(self):
        for i in range(0, len(self.listaListos)):
            self.listaListos[i].masretorno()
    
    def verificarNuevos(self):
        if (len(self.listaNuevos) != 0):
            if (self.tecnica == 'SJF'):
                self.listaNuevos.sort(key=lambda x: x.t_irrupcion)
            eliminados=[]
            for i in range(0, len(self.listaNuevos)):
                indice = self.buscarParticion(self.listaNuevos[i].tamaño)
                if(self.particiones[indice].tamaño>= self.listaNuevos[i].tamaño) and (indice != 0):
                    self.particiones[indice].asignar_part(self.listaNuevos[i])
                    self.agregarListo(self.listaNuevos[i])
                    eliminados.append(self.listaNuevos[i].id)
            for i in range(0, len(eliminados)):
                self.eliminarNuevo(eliminados[i])

                
    def procesar(self):  
        if (self.tecnica == 'SJF'):
            self.procesarSJF()
        else: 
            if (self.tecnica == 'R.R'):
                self.procesarRR()

    def retroceder_tiempo(self):
        self.tiempo_actual= self.tiempo_actual -1

    def procesarRR(self):
        self.pararxContexto = False
        if (len(self.listaListos) != 0):
            if(self.cpu.proceso == ''):
                self.cpu.asignar_cpu(self.listaListos[0])
            else:
                self.cpu.q_restante = self.cpu.q_restante - 1
                self.cpu.proceso.t_restante = self.cpu.proceso.t_restante - 1
                if (self.cpu.proceso.t_restante == 0):
                    self.pararxContexto = True
                    self.eliminarListo(self.cpu.proceso.id)
                    self.agregarTerminado(self.cpu.proceso)
                    self.desasignar_particion(self.cpu.proceso.particion)
                    self.cpu.desasignar_cpu()
                    self.verificarAdmitidos()
                    self.verificarNuevos()
                    if (len(self.listaListos) != 0):
                        self.cpu.asignar_cpu(self.listaListos[0])
                else: 
                    if (self.cpu.q_restante == 0):
                        self.pararxContexto = True
                        self.eliminarListo(self.cpu.proceso.id)
                        self.agregarListo(self.cpu.proceso)
                        self.cpu.desasignar_cpu()
                        if (len(self.listaListos) != 0):
                            self.cpu.asignar_cpu(self.listaListos[0])
        #print('TIEMPO :', self.tiempo)
        #print('Q_restante :', self.cpu.q_restante)
        #if(self.cpu.proceso != ''):
        #    print('T_restante : ', self.cpu.proceso.t_restante)
        #    print('En la cpu se encuentra el proceso: ', self.cpu.proceso.id)
        #else:
        #    print('CPU vacia')
        self.verificarAdmitidos()
        self.verificarNuevos()
        self.tiempo = self.tiempo + 1
        self.tiempo_actual = self.tiempo_actual +1
        if (self.cpu.proceso != ''):
            datoscpu = Cpu(self.cpu.proceso.id, self.cpu.proceso.t_restante)
        else:
            datoscpu = ''

        regtiempos = Reg([],[],[],[],self.pararxContexto, datoscpu)
        for proceso in self.listaNoAdmitidos:
            regtiempos.listaNoAdmitidos.append(proceso) 
        for proceso in self.listaNuevos:
            regtiempos.listaNuevos.append(proceso) 
        for proceso in self.listaListos:
            regtiempos.listaListos.append(proceso) 
        for proceso in self.listaTerminados:
            regtiempos.listaTerminados.append(proceso) 
        self.arregloTiempos.append(regtiempos)
        self.agregartiempos()

    
    def BuscarMenorTrabajo(self):
        if(len(self.listaListos) != 0):
            indice = 0
            min = self.listaListos[0].t_irrupcion 
            for i in range (0, len(self.listaListos)):
                if (self.listaListos[i].t_irrupcion < min):
                    indice = i
                    min = self.listaListos[i].t_irrupcion
            return indice 

    def EsCambioContexto(self):
        if (self.arregloTiempos[self.tiempo_actual].CC is True):
            self.pararxContexto = True

    def procesarSJF(self):
        self.pararxContexto = False
        if (len(self.listaListos) != 0):
            if(self.cpu.proceso == ''):
                menor = self.BuscarMenorTrabajo()
                self.cpu.asignar_cpu(self.listaListos[menor])
            else: 
                self.cpu.proceso.t_restante = self.cpu.proceso.t_restante - 1
                if (self.cpu.proceso.t_restante == 0):
                    self.pararxContexto = True
                    self.eliminarListo(self.cpu.proceso.id)
                    self.agregarTerminado(self.cpu.proceso)
                    self.desasignar_particion(self.cpu.proceso.particion)
                    self.cpu.desasignar_cpu()
                    self.verificarAdmitidos()
                    self.verificarNuevos()
                    if(self.cpu.proceso == ''):
                        if (len(self.listaListos) != 0):
                            menor = self.BuscarMenorTrabajo()
                            self.cpu.asignar_cpu(self.listaListos[menor])     
        #print('TIEMPO :', self.tiempo)
        #if(self.cpu.proceso != ''):
        #    print('T_restante : ', self.cpu.proceso.t_restante)
        #    print('En la cpu se encuentra el proceso: ', self.cpu.proceso.id)
        #else:
        #    print('CPU vacia')
        self.verificarAdmitidos()
        self.verificarNuevos()
        self.tiempo = self.tiempo + 1
        self.tiempo_actual = self.tiempo_actual +1
        if (self.cpu.proceso != ''):
            datoscpu = Cpu(self.cpu.proceso.id, self.cpu.proceso.t_restante)
        else:
            datoscpu = ''

        regtiempos = Reg([],[],[],[],self.pararxContexto, datoscpu)
        for proceso in self.listaNoAdmitidos:
            regtiempos.listaNoAdmitidos.append(proceso) 
        for proceso in self.listaNuevos:
            regtiempos.listaNuevos.append(proceso) 
        for proceso in self.listaListos:
            regtiempos.listaListos.append(proceso) 
        for proceso in self.listaTerminados:
            regtiempos.listaTerminados.append(proceso) 
        self.arregloTiempos.append(regtiempos)
        self.agregartiempos()

    def Reiniciar(self):
        self.listaNuevos= []  # Lo eliminamos de la lista   
        self.listaListos= [] # Lo eliminamos de la lista
        self.listaTerminados = []
        self.listaNoAdmitidos = []
        for particion in self.particiones:
            particion.proceso = ''
            particion.tamaño_restante = particion.tamaño
        self.tiempo = 0
        self.eliminarCpu()
        self.crearCpu()
        self.tiempo_actual = 0
        self.arregloTiempos= []
        self.iniciales = 0
        self.tiempoRetornoProm= 0
        self.tiempoEsperaProm = 0
        self.rendimiento = 0
        self.pararxContexto = False



"""
sim = Simulador('SJF', 'B.F', 150, 5)

sim.abrirArchivo('procesos.txt')

sim.crearCpu()


part1 = Particion(1, 50)
part2 = Particion(2, 150)
part3 = Particion(3, 350)


sim.crearParticion(part1)
sim.crearParticion(part2)
sim.crearParticion(part3)


sim.verificarAdmitidos()
sim.verificarNuevos()


print('Tiempo: ', sim.tiempo_actual)

sim.procesar()
print('Tiempo: ', sim.tiempo_actual)
for i in range(0, len(sim.listaNoAdmitidos)):
 print('No admitidos',sim.arregloTiempos[sim.tiempo_actual- 1].NoAdmitidos[i].id)
for i in range(0, len(sim.listaListos)):
 print('Listos',sim.arregloTiempos[sim.tiempo_actual- 1].Listos[0].id)
    
sim.procesar()
print('Tiempo: ', sim.tiempo_actual)
for i in range(0, len(sim.listaNoAdmitidos)):
 print('No admitidos', sim.arregloTiempos[sim.tiempo_actual-1].NoAdmitidos[i].id)
for i in range(0, len(sim.listaListos)):
 print('Listos',sim.arregloTiempos[sim.tiempo_actual- 1].Listos[i].id)
"""