from Simulador import Simulador
from Particion import Particion

sim = Simulador('R.R', 'W.F', 150, 3)

sim.abrirArchivo('procesos.txt')

sim.crearCpu()


part1 = Particion(1, 150)
part2 = Particion(2, 300)
part3 = Particion(3, 400)


sim.crearParticion(part1)
sim.crearParticion(part2)
sim.crearParticion(part3)


sim.verificarAdmitidos()
sim.verificarNuevos()

while (len(sim.listaTerminados)< sim.iniciales):
    sim.procesar()


    for i in range(1,len(sim.particiones)):
        print('La particion ',sim.particiones[i].id,' espacio disponible', sim.particiones[i].tamaño_restante)
        if (sim.particiones[i].proceso != ''):
            print('tiene a', sim.particiones[i].proceso.id)
    
    print('Lista Nuevos :')
    for i in range(0,len(sim.listaNuevos)):
        print( sim.listaNuevos[i].id)
    print('Lista listos')
    for i in range(0,len(sim.listaListos)):
        print( sim.listaListos[i].id)
    print('Lista Terminados :')
    for i in range(0,len(sim.listaTerminados)):
        print( sim.listaTerminados[i].id)
    
    print('===========================================================================')


for i in range(0, len(sim.listaTerminados)):
    print("ID :", sim.listaTerminados[i].id)
    print("RETORNO :", sim.listaTerminados[i].t_retorno)
    print("ESPERA :", sim.listaTerminados[i].t_espera)
    print(" ")

print("PROMEDIO RETORNO :", sim.tiempoRetornoProm)
print("PROMEDIO ESPERA : ", sim.tiempoEsperaProm)
print("RENDIMIENTO : ", sim.rendimiento, " trabajos por segundo")
