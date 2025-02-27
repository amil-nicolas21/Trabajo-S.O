import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Simulador import Simulador
from Particion import Particion


class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Memoria y Procesos")
        
        self.simulador = Simulador('SJF', 'B.F', 150, 5)
        self.simulador.crearCpu() 
        
        if (self.simulador.seleccion_part=='B.F'):
            selc_part = 'Best Fit'
        else:
            if(self.simulador.seleccion_part == 'W.F'):
                selc_part = 'Worst Fit'

        if(self.simulador.tecnica == 'SJF'):
            tecnica = 'SJF'
        else: 
            if(self.simulador.tecnica == 'R.R'):
                tecnica = 'Round Robin Quantum :' + str(self.simulador.quantum)


        part1 = Particion(1, 50)
        part2 = Particion(2, 150)
        part3 = Particion(3, 350)

        self.simulador.crearParticion(part1)
        self.simulador.crearParticion(part2)
        self.simulador.crearParticion(part3)

        # Texto de Multiprogramación arriba de todo
        self.info = tk.StringVar()
        self.info.set(f"Politica de Asignación de Memoria:  {selc_part}         Planificacion CPU:  {tecnica}           Multiprogramación:  {str(self.simulador.multiprogramacion)}")
        
        multiprogramacion_label = ttk.Label(root, textvariable =self.info, font=("Arial", 12, "bold"))
        multiprogramacion_label.grid(row=0, column=0, columnspan=1, pady=3)
        # Marco principal
        main_frame = ttk.Frame(root, padding="5")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Particiones de Memoria
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Tamaño", "Estado", "ID Proceso", "Fragmentación"), show='headings', height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tamaño", text="Tamaño")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("ID Proceso", text="ID Proceso")
        self.tree.heading("Fragmentación", text="Fragmentación")
        self.tree.grid(row=0, column=1, columnspan=2, padx=0, pady=0, sticky=(tk.W, tk.E))
        
        self.tree.column("ID", width=100)
        self.tree.column("Tamaño", width=150)
        self.tree.column("Estado", width=150)
        self.tree.column("ID Proceso", width=100)
        self.tree.column("Fragmentación", width=150)
        # Panel de Procesos

        abajo_frame = ttk.Frame(main_frame, padding="5")  # Reducido el padding
        abajo_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))
        
        proceso_frame1 = ttk.Frame(main_frame, padding="10")
        proceso_frame1.grid(row=0, column=0, sticky=(tk.N, tk.S))

        proceso_frame = ttk.Frame(main_frame, padding="10")
        proceso_frame.grid(row=0, column=4, sticky=(tk.N, tk.S))
        
        """NUEVO"""
        ttk.Label(abajo_frame, text="                                               ").grid(row=0, column=0, padx=20)
        ttk.Label(abajo_frame, text = "Listos").grid(row=0, column=1, padx=10)
        #self. listos = tk.Listbox(abajo_frame, height=3)
        #self.listos.grid(row=1, column=1, pady=2)  # Reducido el espacio vertical

        self.listos = ttk.Treeview(abajo_frame, columns=("ID", "Tam", "TI"), show='headings', height=3)
        self.listos.heading("ID", text="Id")
        self.listos.heading("Tam", text="Tam")
        self.listos.heading("TI", text="Ti")
        self.listos.grid(row=1, column=1, columnspan=2, padx=0, pady=0, sticky=(tk.W, tk.E))
        
        self.listos.column("ID", width=20)
        self.listos.column("Tam", width=20)
        self.listos.column("TI", width=20)
        
        ttk.Label(abajo_frame, text="                       ").grid(row=0, column=2, padx=20)

        self.ejecutando = tk.StringVar()
        if(self.simulador.cpu.proceso != ''):
            self.ejecutando.set(self.simulador.cpu.proceso.id)
        else: 
            self.ejecutando.set("Ninguno")
        
        ttk.Label(abajo_frame, text="   En Ejecución:", font=("Arial", 10, "bold")).grid(row=0, column=4)
        self.ejecucion_label = ttk.Label(abajo_frame, textvariable= self.ejecutando, font=("Arial", 10, "bold"))
        self.ejecucion_label.grid(row=0, column=5)

        self.tiempo_rest = tk.StringVar()
        if (self.simulador.cpu.proceso != ''):
            self.tiempo_rest.set(f"{self.simulador.cpu.proceso.t_restante}")
        else:
            self.tiempo_rest.set("0")
        ttk.Label(abajo_frame, text='       Tiempo restante: ', font=("Arial", 10, "bold")).grid(row= 1, column = 4)
        
        self.tiempoRest_label = ttk.Label(abajo_frame, textvariable= self.tiempo_rest, font=("Arial", 10, "bold"))
        self.tiempoRest_label.grid(row=1, column=5)
        
        ttk.Label(proceso_frame1, text="No Admitidos").grid(row=0, column=0)

        self.q_restante = tk.StringVar()
        self.q_restante.set('')
        ttk.Label(abajo_frame, textvariable=self.q_restante, font=("Arial", 10, "bold")).grid(row= 1, column = 6)


        self.noAdmitidos = ttk.Treeview(proceso_frame1, columns=("ID", "Tam", "TA", "TI"), show='headings', height=10)
        self.noAdmitidos.heading("ID", text="Id")
        self.noAdmitidos.heading("Tam", text="Tam")
        self.noAdmitidos.heading("TA", text="Ta")
        self.noAdmitidos.heading("TI", text="Ti")
        self.noAdmitidos.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky=(tk.W, tk.E))
        
        self.noAdmitidos.column("ID", width=3)
        self.noAdmitidos.column("Tam", width=10)
        self.noAdmitidos.column("TA", width=10)
        self.noAdmitidos.column("TI", width=10)

        ttk.Label(proceso_frame1, text="Nuevos").grid(row=11, column=0)

        #self.nuevos = tk.Listbox(proceso_frame1, height=5)
        #self.nuevos.grid(row=12, column=0, pady=5)

        self.nuevos = ttk.Treeview(proceso_frame1, columns=("ID", "Tam", "TA", "TI"), show='headings', height=5)
        self.nuevos.heading("ID", text="Id")
        self.nuevos.heading("Tam", text="Tam")
        self.nuevos.heading("TA", text="Ta")
        self.nuevos.heading("TI", text="Ti")
        self.nuevos.grid(row=12, column=0, columnspan=2, padx=0, pady=0, sticky=(tk.W, tk.E))
        
        self.nuevos.column("ID", width=30)
        self.nuevos.column("Tam", width=30)
        self.nuevos.column("TA", width=30)
        self.nuevos.column("TI", width=30)
        """NUEVO"""

        ttk.Label(proceso_frame, text="Procesos Terminados:").grid(row=0, column=0)
        #self.terminados = tk.Listbox(proceso_frame, height=10)
        #self.terminados.grid(row=1, column=0, pady=5)
        self.terminados = ttk.Treeview(proceso_frame, columns=("ID", "TR", "TE"), show='headings', height=10)
        self.terminados.heading("ID", text="Id")
        self.terminados.heading("TR", text="Tr")
        self.terminados.heading("TE", text="Te")
        self.terminados.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky=(tk.W, tk.E))
        
        self.terminados.column("ID", width=25)
        self.terminados.column("TR", width=25)
        self.terminados.column("TE", width=25)

        ttk.Label(proceso_frame, text= ' ').grid(row=5, column=0)
        ttk.Label(proceso_frame, text= ' ').grid(row=6, column=0)


        self.retornoprom = tk.StringVar()
        self.retornoprom.set("Tiempo Retorno Promedio: 0")
        ttk.Label(proceso_frame, textvariable= self.retornoprom).grid(row=7, column=0)

        self.esperaprom = tk.StringVar()
        self.esperaprom.set("Tiempo Espera Promedio: 0")
        ttk.Label(proceso_frame, textvariable= self.esperaprom).grid(row=8, column=0)

        self.rendsist = tk.StringVar()
        self.rendsist.set("Rendimiento del Sistema: 0 t/s")
        ttk.Label(proceso_frame, textvariable= self.rendsist).grid(row=9, column=0)
        
        self.tiempo = tk.StringVar()
        self.tiempo.set(f"Tiempo Actual : {str(self.simulador.tiempo)}")
        ttk.Label(abajo_frame, textvariable =self.tiempo, font=("Arial", 12, "bold")).grid(row=1, column= 0)
        
        # Controles
        control_frame = ttk.Frame(root, padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.cargar_btn = ttk.Button(control_frame, text="Cargar desde Archivo", command=self.cargar_archivo)
        self.cargar_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.avanzar_btn = ttk.Button(control_frame, text="Avanzar Tiempo", command=self.avanzar_tiempo)
        self.avanzar_btn.grid(row=0, column=1, padx=5, pady=5)

        self.avanzar_btn = ttk.Button(control_frame, text="Avanzar a Cambio de Contexto", command=self.avanzar_ccontexto)
        self.avanzar_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.retroceder_btn = ttk.Button(control_frame, text="Retroceder Tiempo", command=self.retroceder_tiempo)
        self.retroceder_btn.grid(row=0, column=3, padx=5, pady=5)

        self.retrocederCC_btn = ttk.Button(control_frame, text="Retroceder Cambio de Contexto", command=self.retroceder_hCC)
        self.retrocederCC_btn.grid(row=0, column=4, padx=5, pady=5)
        
        self.actualizar_btn = ttk.Button(control_frame, text="Reiniciar Simulador", command=self.reiniciar_simulador)
        self.actualizar_btn.grid(row=0, column=5, padx=5, pady=5)

        self.config_btn = ttk.Button(control_frame, text="Configuraciones", command=self.abrir_configuraciones)
        self.config_btn.grid(row=0, column=6, padx=5, pady=5)
        self.actualizar_interfaz()
        
    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            self.simulador.abrirArchivo(file_path)
            self.actualizar_interfaz()
        
    def actualizar_interfaz(self):
        if (self.simulador.seleccion_part=='B.F'):
            selc_part = 'Best Fit'
        else:
            if(self.simulador.seleccion_part == 'W.F'):
                selc_part = 'Worst Fit'

        if(self.simulador.tecnica == 'SJF'):
            tecnica = 'SJF'
        else: 
            if(self.simulador.tecnica == 'R.R'):
                tecnica = 'Round Robin Quantum :' + str(self.simulador.quantum)
                self.q_restante.set(f'       Quantum restante:  {self.simulador.cpu.q_restante}')

        self.info.set(f"Politica de Asignación de Memoria:  {selc_part}         Planificacion CPU:  {tecnica}           Multiprogramación:  {str(self.simulador.multiprogramacion)}")

        for item in self.tree.get_children(): 
            self.tree.delete(item)

        if (self.simulador.tiempo==self.simulador.tiempo_actual):
            padre = self.simulador
            cpu = self.simulador.cpu.proceso
            for particion in self.simulador.particiones:
                if (particion.id == 0):
                    self.tree.insert("", "end", values=(particion.id, particion.tamaño, "Sistema Operativo", particion.proceso.id if particion.proceso else "", particion.tamaño_restante))
                else: 
                    self.tree.insert("", "end", values=(particion.id, particion.tamaño, "Libre" if particion.proceso == '' else "Ocupado", particion.proceso.id if particion.proceso else "", particion.tamaño_restante))
        else:
            padre = self.simulador.arregloTiempos[self.simulador.tiempo_actual-1]
            cpu = self.simulador.arregloTiempos[self.simulador.tiempo_actual-1].cpu
            x= 0
            if(padre.listaListos):
                padre.listaListos.sort(key=lambda x: x.particion)
            for particion in self.simulador.particiones:
                if (particion.id == 0):
                    self.tree.insert("", "end", values=(particion.id, particion.tamaño, "Sistema Operativo", particion.proceso.id if particion.proceso else "", particion.tamaño_restante))
                else:
                    if (particion.id == padre.listaListos[x].particion):
                        self.tree.insert("", "end", values=(particion.id, particion.tamaño, "Ocupado", padre.listaListos[x].id, (particion.tamaño -padre.listaListos[x].tamaño)))
                        x= x +1
                    else:
                        self.tree.insert("", "end", values=(particion.id, particion.tamaño, "Libre", "", particion.tamaño))

        
        for item in self.terminados.get_children(): 
            self.terminados.delete(item)

        for proceso in padre.listaTerminados:
            self.terminados.insert("", "end", values=(proceso.id, proceso.t_retorno ,proceso.t_espera))

        """Nuevo"""

        for item in self.noAdmitidos.get_children(): 
            self.noAdmitidos.delete(item)
        for proceso in padre.listaNoAdmitidos:
            self.noAdmitidos.insert("", "end", values=(proceso.id, proceso.tamaño, proceso.t_arribo, proceso.t_irrupcion))
        
        for item in self.nuevos.get_children(): 
            self.nuevos.delete(item)
        for proceso in padre.listaNuevos:
            self.nuevos.insert("", "end", values=(proceso.id, proceso.tamaño, proceso.t_arribo, proceso.t_irrupcion))

        for item in self.listos.get_children(): 
            self.listos.delete(item)
        for proceso in padre.listaListos:
            self.listos.insert("", "end", values=(proceso.id, proceso.tamaño, proceso.t_irrupcion))

        if(cpu != ''):
            self.ejecutando.set(cpu.id)
            self.tiempo_rest.set(f"{cpu.t_restante}")
        else: 
            self.ejecutando.set("Ninguno")
            self.tiempo_rest.set("0")

        if(self.simulador.tiempoRetornoProm != ''):
            self.retornoprom.set(f"Tiempo Retorno Promedio: {round(self.simulador.tiempoRetornoProm,2)}")
            self.esperaprom.set(f"Tiempo Espera Promedio: {round(self.simulador.tiempoEsperaProm,2)}")
            self.rendsist.set(f"Rendimiento del Sistema: {round(self.simulador.rendimiento, 2)} t/s")


        if (self.simulador.tiempo_actual != 0):
            self.tiempo.set(f"Tiempo Actual : {self.simulador.tiempo_actual - 1}")
    
    def retroceder_tiempo(self):
        if (self.simulador.tiempo_actual>1):
            self.simulador.retroceder_tiempo()
            self.actualizar_interfaz()
        else:
            messagebox.showinfo('ADVERTENCIA', 'No se puede volver atrás')
    
    def retroceder_hCC(self):
        while (self.simulador.pararxContexto != True and self.simulador.tiempo_actual>1):
            self.simulador.retroceder_tiempo()
            self.simulador.EsCambioContexto()
            self.actualizar_interfaz()
        self.simulador.pararxContexto = False

            

        
    def avanzar_tiempo(self):
        if (self.simulador.iniciales == 0):
            messagebox.showerror('ERROR', 'No se seleccionó un archivo')
        else:
            if (self.simulador.iniciales == len(self.simulador.listaTerminados)):
                messagebox.showerror('ERROR', 'Todos los procesos han terminado')
            else:
                if(self.simulador.tiempo == self.simulador.tiempo_actual):
                    self.simulador.verificarAdmitidos()
                    self.simulador.verificarNuevos()
                    self.simulador.procesar()
                else:
                    self.simulador.tiempo_actual = self.simulador.tiempo_actual + 1
                self.actualizar_interfaz()
    
    def avanzar_ccontexto(self):
        if (self.simulador.iniciales == 0):
            messagebox.showerror('ERROR', 'No se seleccionó un archivo')
        else:
            if (self.simulador.iniciales == len(self.simulador.listaTerminados)):
                messagebox.showerror('ERROR', 'Todos los procesos han terminado')
            else:
                while(self.simulador.pararxContexto != True):
                    if(self.simulador.tiempo == self.simulador.tiempo_actual):
                        self.simulador.verificarAdmitidos()
                        self.simulador.verificarNuevos()
                        self.simulador.procesar()
                    else:
                        self.simulador.EsCambioContexto()
                        self.simulador.tiempo_actual = self.simulador.tiempo_actual + 1
                    self.actualizar_interfaz()
                self.simulador.pararxContexto = False

    def reiniciar_simulador(self):
        self.simulador.Reiniciar()
        self.actualizar_interfaz()

    def abrir_configuraciones(self):
        # Crear la ventana emergente
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuraciones de CPU")

        # Política de asignación (Ejemplo con ComboBox)
        ttk.Label(config_window, text="Política de Asignación:").grid(row=0, column=0, padx=10, pady=10)
        self.politica_asignacion_combobox = ttk.Combobox(config_window, values=["Best Fit", "Worst Fit"])
        self.politica_asignacion_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Política de planificación (Ejemplo con ComboBox)
        ttk.Label(config_window, text="Planificación CPU:").grid(row=1, column=0, padx=10, pady=10)
        self.politica_planificacion_combobox = ttk.Combobox(config_window, values=["SJF", "Round Robin"])
        self.politica_planificacion_combobox.grid(row=1, column=1, padx=10, pady=10)
        
        self.politica_planificacion_combobox.bind("<<ComboboxSelected>>", self.mostrar_quantum)

        # Campo de entrada para el quantum, inicialmente oculto
        self.quantum_label = ttk.Label(config_window, text="Quantum:")
        self.quantum_label.grid(row=2, column=0, padx=10, pady=10)
        self.quantum_label.grid_forget()  # Ocultar inicialmente

        self.quantum_entry = ttk.Entry(config_window)
        self.quantum_entry.grid(row=2, column=1, padx=10, pady=10)
        self.quantum_entry.grid_forget()  # Ocultar inicialmente

        # Botón para guardar las configuraciones
        guardar_btn = ttk.Button(config_window, text="Guardar Configuraciones", command=self.guardar_configuraciones)
        guardar_btn.grid(row=3, column=0, columnspan=2, pady=10)
    
    def mostrar_quantum(self, event):
        # Mostrar u ocultar el campo del quantum si se selecciona Round Robin
        if self.politica_planificacion_combobox.get() == "Round Robin":
            self.quantum_label.grid(row=2, column=0, padx=10, pady=10)
            self.quantum_entry.grid(row=2, column=1, padx=10, pady=10)
        else:
            self.quantum_label.grid_forget()
            self.quantum_entry.grid_forget()
    
    def es_numero(self, valor):
        # Verifica si el valor es un número (puede ser entero o decimal)
        try:
            float(int(valor))  # Intentar convertirlo a número
            return True
        except ValueError:
            return False

    def guardar_configuraciones(self):
        politica_asignacion = self.politica_asignacion_combobox.get()
        politica_planificacion = self.politica_planificacion_combobox.get()

        if (politica_asignacion== "Worst Fit"):
            politica_asignacion = "W.F"
        else:
            politica_asignacion = "B.F"
        if(politica_planificacion == "Round Robin"):
            politica_planificacion = "R.R"
        else:
            politica_planificacion = "SJF"

        if politica_planificacion == "R.R":
            quantum = self.quantum_entry.get()
            if not self.es_numero(quantum):
                # Si el valor no es un número, mostrar mensaje de advertencia
                messagebox.showerror("ERROR", "El valor del Quantum debe ser un número válido.")
                return
        else:
            quantum = ''
        
        self.simulador.tecnica= politica_planificacion
        self.simulador.seleccion_part= politica_asignacion
        self.simulador.quantum= quantum
        self.reiniciar_simulador()
        

            
    
        
if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()
