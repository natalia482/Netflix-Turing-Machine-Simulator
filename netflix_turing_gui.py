import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import threading
import time

class NetflixTuringMachineGUI:
    def __init__(self, tape=None):
        # Inicializar la cinta con películas si no se proporciona
        if tape is None:
            self.tape = ["P1", "P2", "P3", "P4", "P5", "B", "B"]
        else:
            self.tape = tape
        
        # Establecer posición inicial y estado
        self.head_position = 0
        self.state = "NAVIGATE"
        self.watched = set()
        
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Netflix Turing Machine Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0f0f0f')
        
        # Variables de control
        self.auto_mode = False
        self.auto_thread = None
        
        # Configurar la interfaz
        self.setup_gui()
        self.update_display()
    
    def setup_gui(self):
        """Configura la interfaz gráfica."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#0f0f0f')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="SIMULACIÓN DE NETFLIX CON MÁQUINA DE TURING",
            font=("Arial", 18, "bold"),
            fg='#e50914',
            bg='#0f0f0f'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame superior para la cinta y controles
        upper_frame = tk.Frame(main_frame, bg='#0f0f0f')
        upper_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame izquierdo para la visualización
        left_frame = tk.Frame(upper_frame, bg='#0f0f0f')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame derecho para el terminal
        right_frame = tk.Frame(upper_frame, bg='#0f0f0f')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Configurar la sección de visualización
        self.setup_visualization_section(left_frame)
        
        # Configurar la sección del terminal
        self.setup_terminal_section(right_frame)
        
        # Frame inferior para controles generales
        control_frame = tk.Frame(main_frame, bg='#0f0f0f')
        control_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botones de control general
        self.setup_general_controls(control_frame)
    
    def setup_visualization_section(self, parent):
        """Configura la sección de visualización de la máquina."""
        # Título de la sección
        viz_title = tk.Label(
            parent,
            text="VISUALIZACIÓN DE LA MÁQUINA",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#0f0f0f'
        )
        viz_title.pack(pady=(0, 15))
        
        # Frame para información del estado
        state_frame = tk.Frame(parent, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        state_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Estado actual
        self.state_label = tk.Label(
            state_frame,
            text="Estado: NAVIGATE",
            font=("Arial", 12, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        self.state_label.pack(pady=10)
        
        # Posición del cabezal
        self.position_label = tk.Label(
            state_frame,
            text="Posición del cabezal: 0",
            font=("Arial", 11),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        self.position_label.pack(pady=(0, 10))
        
        # Frame para la cinta
        tape_frame = tk.Frame(parent, bg='#0f0f0f')
        tape_frame.pack(fill=tk.X, pady=(0, 15))
        
        tape_label = tk.Label(
            tape_frame,
            text="CINTA DE PELÍCULAS",
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#0f0f0f'
        )
        tape_label.pack(pady=(0, 10))
        
        # Frame para los elementos de la cinta
        self.tape_frame = tk.Frame(tape_frame, bg='#0f0f0f')
        self.tape_frame.pack()
        
        # Crear elementos de la cinta
        self.tape_elements = []
        for i, item in enumerate(self.tape):
            self.create_tape_element(i, item)
        
        # Frame para información adicional
        info_frame = tk.Frame(parent, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.info_label = tk.Label(
            info_frame,
            text="Navegando por el catálogo",
            font=("Arial", 11),
            fg='#ffffff',
            bg='#1a1a1a',
            wraplength=400
        )
        self.info_label.pack(pady=10)
        
        # Frame para acciones disponibles
        actions_frame = tk.Frame(parent, bg='#0f0f0f')
        actions_frame.pack(fill=tk.X)
        
        actions_title = tk.Label(
            actions_frame,
            text="ACCIONES DISPONIBLES",
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#0f0f0f'
        )
        actions_title.pack(pady=(0, 10))
        
        # Frame para botones de acción
        self.buttons_frame = tk.Frame(actions_frame, bg='#0f0f0f')
        self.buttons_frame.pack()
    
    def setup_terminal_section(self, parent):
        """Configura la sección del terminal."""
        # Título de la sección
        terminal_title = tk.Label(
            parent,
            text="REGISTRO DE ACTIVIDAD",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#0f0f0f'
        )
        terminal_title.pack(pady=(0, 10))
        
        # Área de texto para el terminal
        self.terminal_text = scrolledtext.ScrolledText(
            parent,
            height=35,
            width=50,
            bg='#000000',
            fg='#00ff00',
            font=("Courier", 10),
            insertbackground='#00ff00',
            selectbackground='#333333'
        )
        self.terminal_text.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial en el terminal
        self.log_to_terminal("=" * 50)
        self.log_to_terminal("SIMULACIÓN DE NETFLIX CON MÁQUINA DE TURING")
        self.log_to_terminal("=" * 50)
        self.log_to_terminal("Sistema inicializado correctamente.")
        self.log_to_terminal("Estado inicial: NAVIGATE")
        self.log_to_terminal("Posición inicial del cabezal: 0")
        self.log_to_terminal("=" * 50)
    
    def setup_general_controls(self, parent):
        """Configura los controles generales."""
        # Botón de modo automático
        self.auto_button = tk.Button(
            parent,
            text="ACTIVAR MODO AUTOMÁTICO",
            command=self.toggle_auto_mode,
            font=("Arial", 11, "bold"),
            bg='#e50914',
            fg='#ffffff',
            activebackground='#f40612',
            activeforeground='#ffffff',
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=5
        )
        self.auto_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón de reinicio
        reset_button = tk.Button(
            parent,
            text="REINICIAR SIMULACIÓN",
            command=self.reset_simulation,
            font=("Arial", 11, "bold"),
            bg='#333333',
            fg='#ffffff',
            activebackground='#555555',
            activeforeground='#ffffff',
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=5
        )
        reset_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Etiqueta de contenido visto
        watched_label = tk.Label(
            parent,
            text="Contenido visto:",
            font=("Arial", 11, "bold"),
            fg='#ffffff',
            bg='#0f0f0f'
        )
        watched_label.pack(side=tk.LEFT, padx=(20, 10))
        
        self.watched_display = tk.Label(
            parent,
            text="Ninguno",
            font=("Arial", 11),
            fg='#00ff00',
            bg='#0f0f0f'
        )
        self.watched_display.pack(side=tk.LEFT)
    
    def create_tape_element(self, index, item):
        """Crea un elemento visual de la cinta."""
        # Determinar el color según el tipo de contenido
        if item.startswith('P'):
            if item in self.watched:
                bg_color = '#006600'  # Verde para visto
                text_color = '#ffffff'
            else:
                bg_color = '#e50914'  # Rojo Netflix para no visto
                text_color = '#ffffff'
        else:
            bg_color = '#333333'  # Gris para espacios en blanco
            text_color = '#666666'
        
        # Crear el frame del elemento
        element_frame = tk.Frame(self.tape_frame, bg='#0f0f0f')
        element_frame.pack(side=tk.LEFT, padx=2)
        
        # Etiqueta del índice
        index_label = tk.Label(
            element_frame,
            text=str(index),
            font=("Arial", 8),
            fg='#888888',
            bg='#0f0f0f'
        )
        index_label.pack()
        
        # Elemento de la cinta
        element = tk.Label(
            element_frame,
            text=item + ("✓" if item in self.watched else ""),
            font=("Arial", 12, "bold"),
            bg=bg_color,
            fg=text_color,
            width=4,
            height=2,
            relief=tk.RAISED if index == self.head_position else tk.FLAT,
            bd=3 if index == self.head_position else 1
        )
        
        # Resaltar el cabezal actual
        if index == self.head_position:
            element.configure(relief=tk.RAISED, bd=4)
            # Agregar flecha indicadora
            arrow_label = tk.Label(
                element_frame,
                text="▲",
                font=("Arial", 12, "bold"),
                fg='#ffff00',
                bg='#0f0f0f'
            )
            arrow_label.pack()
        
        element.pack()
        self.tape_elements.append((element_frame, element))
    
    def update_tape_display(self):
        """Actualiza la visualización de la cinta."""
        # Limpiar elementos existentes
        for frame, element in self.tape_elements:
            frame.destroy()
        self.tape_elements.clear()
        
        # Recrear elementos
        for i, item in enumerate(self.tape):
            self.create_tape_element(i, item)
    
    def create_action_buttons(self):
        """Crea los botones de acción según el estado actual."""
        # Limpiar botones existentes
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        # Obtener acciones disponibles
        available_actions = self.get_available_actions()
        
        # Crear botones para cada acción
        for action in available_actions:
            button_text, button_color = self.get_button_properties(action)
            
            button = tk.Button(
                self.buttons_frame,
                text=button_text,
                command=lambda a=action: self.execute_action(a),
                font=("Arial", 10, "bold"),
                bg=button_color,
                fg='#ffffff',
                activebackground=self.lighten_color(button_color),
                activeforeground='#ffffff',
                relief=tk.RAISED,
                bd=2,
                padx=15,
                pady=5,
                width=15
            )
            button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def get_button_properties(self, action):
        """Obtiene las propiedades del botón según la acción."""
        properties = {
            'R': ("MOVER →", "#007acc"),
            'L': ("← MOVER", "#007acc"),
            'select': ("SELECCIONAR", "#e50914"),
            'play': ("REPRODUCIR", "#00aa00"),
            'mark_watched': ("MARCAR VISTO", "#ff8800"),
            'back': ("VOLVER", "#666666"),
            'quit': ("SALIR", "#cc0000")
        }
        return properties.get(action, (action.upper(), "#333333"))
    
    def lighten_color(self, color):
        """Aclara un color hexadecimal para el efecto hover."""
        if color.startswith('#'):
            color = color[1:]
        
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter_rgb = tuple(min(255, int(c * 1.3)) for c in rgb)
        return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
    
    def get_available_actions(self):
        """Devuelve las acciones disponibles según el estado actual."""
        current_item = self.tape[self.head_position] if 0 <= self.head_position < len(self.tape) else "B"
        
        if self.state == "NAVIGATE":
            actions = []
            if self.head_position < len(self.tape) - 1:
                actions.append('R')
            if self.head_position > 0:
                actions.append('L')
            if current_item.startswith('P'):
                actions.append('select')
            actions.append('quit')
            return actions
        
        elif self.state == "SELECT":
            actions = ['back']
            if current_item.startswith('P'):
                actions.append('play')
            return actions
        
        elif self.state == "PLAY":
            actions = ['back']
            if current_item.startswith('P') and current_item not in self.watched:
                actions.append('mark_watched')
            return actions
        
        return []
    
    def execute_action(self, action):
        """Ejecuta una acción y actualiza el estado."""
        if self.auto_mode:
            return  # No permitir acciones manuales en modo automático
        
        self.process_action(action)
        self.update_display()
    
    def process_action(self, action):
        """Procesa una acción específica."""
        current_item = self.tape[self.head_position] if 0 <= self.head_position < len(self.tape) else "B"
        
        if self.state == "NAVIGATE":
            if action == 'select' and current_item.startswith('P'):
                self.state = "SELECT"
                self.log_to_terminal(f"➤ Has seleccionado {current_item}.")
            elif action == 'R':
                if self.head_position < len(self.tape) - 1:
                    self.head_position += 1
                    self.log_to_terminal("➤ Moviendo a la derecha.")
                else:
                    self.log_to_terminal("➤ No puedes moverte más a la derecha.")
            elif action == 'L':
                if self.head_position > 0:
                    self.head_position -= 1
                    self.log_to_terminal("➤ Moviendo a la izquierda.")
                else:
                    self.log_to_terminal("➤ No puedes moverte más a la izquierda.")
            elif action == 'quit':
                self.state = "FINISH"
                self.log_to_terminal("➤ Finalizando por decisión del usuario.")
        
        elif self.state == "SELECT":
            if action == 'play' and current_item.startswith('P'):
                self.state = "PLAY"
                self.log_to_terminal(f"➤ Reproduciendo {current_item}.")
            elif action == 'back':
                self.state = "NAVIGATE"
                self.log_to_terminal("➤ Volviendo al modo de navegación.")
        
        elif self.state == "PLAY":
            if action == 'mark_watched' and current_item.startswith('P'):
                self.watched.add(current_item)
                self.state = "NAVIGATE"
                self.log_to_terminal(f"➤ Has marcado {current_item} como visto.")
            elif action == 'back':
                self.state = "SELECT"
                self.log_to_terminal("➤ Volviendo al modo de selección.")
        
        # Verificar condiciones de finalización
        self.check_finish_conditions()
    
    def check_finish_conditions(self):
        """Verifica si se deben cumplir condiciones de finalización."""
        if self.state == "FINISH":
            self.log_to_terminal("=" * 50)
            self.log_to_terminal("SIMULACIÓN FINALIZADA")
            self.log_to_terminal("=" * 50)
            if self.watched:
                self.log_to_terminal("Contenido visto durante la sesión:")
                for item in sorted(self.watched):
                    self.log_to_terminal(f"- {item}")
            else:
                self.log_to_terminal("No se ha visto ningún contenido.")
    
    def update_display(self):
        """Actualiza toda la visualización."""
        # Actualizar etiquetas de estado
        self.state_label.configure(text=f"Estado: {self.state}")
        self.position_label.configure(text=f"Posición del cabezal: {self.head_position}")
        
        # Actualizar información adicional
        current_item = self.tape[self.head_position] if 0 <= self.head_position < len(self.tape) else "B"
        info_text = self.get_info_text(current_item)
        self.info_label.configure(text=info_text)
        
        # Actualizar cinta
        self.update_tape_display()
        
        # Actualizar botones de acción
        if self.state != "FINISH":
            self.create_action_buttons()
        else:
            # Limpiar botones si la simulación ha terminado
            for widget in self.buttons_frame.winfo_children():
                widget.destroy()
        
        # Actualizar contenido visto
        if self.watched:
            watched_text = ", ".join(sorted(self.watched))
        else:
            watched_text = "Ninguno"
        self.watched_display.configure(text=watched_text)
    
    def get_info_text(self, current_item):
        """Obtiene el texto informativo según el estado actual."""
        if self.state == "NAVIGATE":
            if current_item.startswith('P'):
                status = "✓ VISTO" if current_item in self.watched else "DISPONIBLE"
                return f"Película actual: {current_item} ({status})\nPuedes seleccionar esta película o moverte por el catálogo."
            else:
                return "Espacio en blanco. Muévete para encontrar contenido."
        
        elif self.state == "SELECT":
            return f"Has seleccionado: {current_item}\nPuedes reproducir la película o volver a navegar."
        
        elif self.state == "PLAY":
            return f"Reproduciendo: {current_item}\nPuedes marcar como visto o volver atrás."
        
        elif self.state == "FINISH":
            return "La simulación ha terminado. Puedes reiniciar para comenzar de nuevo."
        
        return "Estado desconocido."
    
    def log_to_terminal(self, message):
        """Registra un mensaje en el terminal."""
        self.terminal_text.insert(tk.END, message + "\n")
        self.terminal_text.see(tk.END)
    
    def toggle_auto_mode(self):
        """Activa o desactiva el modo automático."""
        if not self.auto_mode:
            self.auto_mode = True
            self.auto_button.configure(text="DETENER MODO AUTOMÁTICO", bg='#cc6600')
            self.log_to_terminal("➤ Modo automático activado.")
            
            # Deshabilitar botones de acción
            for widget in self.buttons_frame.winfo_children():
                widget.configure(state=tk.DISABLED)
            
            # Iniciar hilo automático
            self.auto_thread = threading.Thread(target=self.auto_simulation_loop)
            self.auto_thread.daemon = True
            self.auto_thread.start()
        else:
            self.auto_mode = False
            self.auto_button.configure(text="ACTIVAR MODO AUTOMÁTICO", bg='#e50914')
            self.log_to_terminal("➤ Modo automático desactivado.")
            
            # Habilitar botones de acción
            self.update_display()
    
    def auto_simulation_loop(self):
        """Bucle de simulación automática."""
        while self.auto_mode and self.state != "FINISH":
            available_actions = self.get_available_actions()
            
            if not available_actions:
                break
            
            # Seleccionar acción aleatoria
            chosen_action = random.choice(available_actions)
            
            # Ejecutar acción en el hilo principal
            self.root.after(0, lambda: self.process_action(chosen_action))
            self.root.after(0, self.update_display)
            
            # Obtener nombre de acción para el log
            action_names = {
                'R': 'Mover a la derecha',
                'L': 'Mover a la izquierda',
                'select': 'Seleccionar contenido',
                'play': 'Reproducir',
                'mark_watched': 'Marcar como visto',
                'back': 'Volver atrás',
                'quit': 'Salir'
            }
            
            action_name = action_names.get(chosen_action, chosen_action)
            self.root.after(0, lambda: self.log_to_terminal(f"[AUTO] Acción: {action_name}"))
            
            # Pausa entre acciones
            time.sleep(2)
        
        # Desactivar modo automático al finalizar
        if self.auto_mode:
            self.root.after(0, self.toggle_auto_mode)
    
    def reset_simulation(self):
        """Reinicia la simulación."""
        # Detener modo automático si está activo
        if self.auto_mode:
            self.toggle_auto_mode()
        
        # Reiniciar estado
        self.head_position = 0
        self.state = "NAVIGATE"
        self.watched.clear()
        
        # Limpiar terminal
        self.terminal_text.delete(1.0, tk.END)
        
        # Mensaje inicial
        self.log_to_terminal("=" * 50)
        self.log_to_terminal("SIMULACIÓN REINICIADA")
        self.log_to_terminal("=" * 50)
        self.log_to_terminal("Sistema reinicializado correctamente.")
        self.log_to_terminal("Estado inicial: NAVIGATE")
        self.log_to_terminal("Posición inicial del cabezal: 0")
        self.log_to_terminal("=" * 50)
        
        # Actualizar visualización
        self.update_display()
    
    def run(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()


def main():
    """Función principal."""
    # Crear y ejecutar la aplicación
    catalog = ["P1", "P2", "P3", "P4", "P5", "B", "B"]
    app = NetflixTuringMachineGUI(catalog)
    app.run()


if __name__ == "__main__":
    main()