from Simulador import Simulador
from Particion import Particion

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



 
res = ''
while (len(sim.listaTerminados)< sim.iniciales) and (res != '0'):
    print('1. Para avanzar al siguiente tiempo;  2.Para avanzar hasta un cambio de contexto;  0.Para cerrar')
    res = input('Respuesta : ')
    if (res == '1'):
        bandera = False
    while ((res== '1' and bandera == False) or (res == '2' and sim.pararxContexto != True) ):
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
        if (res == '1'): 
            bandera = True
    sim.pararxContexto = False


for i in range(0, len(sim.listaTerminados)):
    print("ID :", sim.listaTerminados[i].id)
    print("RETORNO :", sim.listaTerminados[i].t_retorno)
    print("ESPERA :", sim.listaTerminados[i].t_espera)
    print(" ")

print("PROMEDIO RETORNO :", sim.tiempoRetornoProm)
print("PROMEDIO ESPERA : ", sim.tiempoEsperaProm)
print("RENDIMIENTO : ", sim.rendimiento, " trabajos por segundo")
