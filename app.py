import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importamos el módulo matemático
import matematica as mat

class AppIncendio:
    def __init__(self, root):
        self.root = root
        self.root.title("Módulo 1: Foco de Incendio e Intensidad")
        self.root.geometry("1100x600")
        
        # --- PANEL IZQUIERDO: CONFIGURACIÓN DE PARÁMETROS ---
        panel_control = tk.Frame(root, width=250, padx=15, pady=15, bg="#f0f0f0")
        panel_control.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(panel_control, text="Configuración del Foco", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Entradas de texto para las variables
        self.entry_A = self.crear_campo(panel_control, "Intensidad Inicial (A > 0):", "10.0")
        self.entry_k = self.crear_campo(panel_control, "Dispersión Espacial (k > 0):", "15.0")
        self.entry_x0 = self.crear_campo(panel_control, "Coordenada X del Foco (x0):", "0.0")
        self.entry_y0 = self.crear_campo(panel_control, "Coordenada Y del Foco (y0):", "0.0")
        
        # Botón para renderizar el modelo
        btn_calcular = tk.Button(panel_control, text="Generar Modelo", command=self.procesar_y_graficar, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
        btn_calcular.pack(pady=20)
        
        # --- PANEL DERECHO: ESPACIO PARA LOS GRÁFICOS ---
        self.panel_graficos = tk.Frame(root, bg="white")
        self.panel_graficos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Generar gráfico inicial por defecto
        self.canvas = None
        self.procesar_y_graficar()

    def crear_campo(self, parent, text, default_val):
        """Helper para construir etiquetas y campos de entrada fácilmente"""
        tk.Label(parent, text=text, anchor="w", bg="#f0f0f0").pack(fill=tk.X, pady=(5, 0))
        entry = tk.Entry(parent)
        entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=(0, 5))
        return entry

    def procesar_y_graficar(self):
        try:
            # 1. Recuperar los valores que el usuario ingresó en la interfaz
            A = float(self.entry_A.get())
            k = float(self.entry_k.get())
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            
            # Validación matemática interactiva
            if A <= 0 or k <= 0:
                messagebox.showerror("Error de Parámetros", "Los parámetros A y k deben ser mayores estrictamente que 0.")
                return
                
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, introduce únicamente valores numéricos en los campos.")
            return

        # 2. Consumir la lógica de matematica.py
        X, Y = mat.inicializar_malla(x0, y0, radio_estudio=12, puntos=80)
        Z_foco = mat.calcular_riesgo_foco(X, Y, A, k, x0, y0)

        # 3. Dibujar/Actualizar los gráficos de Matplotlib dentro de Tkinter
        if self.canvas:
            self.canvas.get_tk_widget().destroy() # Limpiar el gráfico anterior si existe
            plt.close('all')

        fig = plt.figure(figsize=(10, 5))
        
        # Subplot 1: Superficie 3D
        ax1 = fig.add_subplot(121, projection='3d')
        superficie = ax1.plot_surface(X, Y, Z_foco, cmap='inferno', edgecolor='none', alpha=0.8)
        ax1.set_title(f'Superficie de Riesgo 3D (A={A}, k={k})', fontsize=10)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        fig.colorbar(superficie, ax=ax1, shrink=0.5, aspect=10)
        
        # Subplot 2: Curvas de Nivel
        ax2 = fig.add_subplot(122)
        curvas = ax2.contour(X, Y, Z_foco, levels=12, cmap='inferno')
        ax2.clabel(curvas, inline=True, fontsize=8)
        ax2.plot(x0, y0, 'ro', label=f'Foco ({x0}, {y0})')
        ax2.set_title('Curvas de Nivel Circulares', fontsize=10)
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.legend()
        
        fig.tight_layout()

        # Incrustar el objeto de matplotlib dentro del contenedor de Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.panel_graficos)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Lanzamiento de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = AppIncendio(root)
    root.mainloop()