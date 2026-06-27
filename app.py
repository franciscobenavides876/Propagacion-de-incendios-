import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importamos el módulo matemático
import matematica as mat

class AppIncendio:
    def __init__(self, root):
        self.root = root
        self.root.title("Módulo Integrado: Foco e Influencia Topográfica")
        self.root.geometry("1200x700")
        
        # --- PANEL IZQUIERDO: CONFIGURACIÓN DE PARÁMETROS ---
        panel_control = tk.Frame(root, width=280, padx=15, pady=15, bg="#f0f0f0")
        panel_control.pack(side=tk.LEFT, fill=tk.Y)
        
        # Parámetros de Fran (Foco)
        tk.Label(panel_control, text="Configuración del Foco", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=(0, 5))
        self.entry_A = self.crear_campo(panel_control, "Intensidad Inicial (A):", "10.0")
        self.entry_k = self.crear_campo(panel_control, "Dispersión Espacial (k):", "15.0")
        self.entry_x0 = self.crear_campo(panel_control, "Coordenada X0:", "0.0")
        self.entry_y0 = self.crear_campo(panel_control, "Coordenada Y0:", "0.0")
        
        # Parámetros de Tomás (Terreno y Vegetación)
        tk.Label(panel_control, text="Configuración del Terreno", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(pady=(15, 5))
        self.entry_alpha = self.crear_campo(panel_control, "Factor Vegetación (alpha):", "0.4")
        self.entry_H = self.crear_campo(panel_control, "Altura Relieve (H):", "3.0")
        self.entry_wx = self.crear_campo(panel_control, "Frecuencia Espacial X (wx):", "0.4")
        self.entry_wy = self.crear_campo(panel_control, "Frecuencia Espacial Y (wy):", "0.4")
        
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
        tk.Label(parent, text=text, anchor="w", bg="#f0f0f0").pack(fill=tk.X, pady=(2, 0))
        entry = tk.Entry(parent)
        entry.insert(0, default_val)
        entry.pack(fill=tk.X, pady=(0, 2))
        return entry

    def procesar_y_graficar(self):
        try:
            # Recuperar parámetros del Foco (Fran)
            A = float(self.entry_A.get())
            k = float(self.entry_k.get())
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            
            # Recuperar parámetros del Terreno (Tomás)
            alpha = float(self.entry_alpha.get())
            H = float(self.entry_H.get())
            wx = float(self.entry_wx.get())
            wy = float(self.entry_wy.get())
            
            # Validaciones básicas
            if A <= 0 or k <= 0 or alpha < 0:
                messagebox.showerror("Error de Parámetros", "A, k y alpha deben cumplir las restricciones físicas.")
                return
                
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, introduce únicamente valores numéricos.")
            return

        # Inicialización de grilla común y cálculo de capas
        X, Y = mat.inicializar_malla(x0, y0, radio_estudio=15, puntos=100)
        Z_foco = mat.calcular_riesgo_foco(X, Y, A, k, x0, y0)
        Z_terreno = mat.calcular_terreno(X, Y, H, wx, wy)
        
        # Unión Lineal del Modelo Completo: P = Foco + alpha * S
        Z_total = Z_foco + alpha * Z_terreno

        # Actualizar componentes de Matplotlib
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            plt.close('all')

        fig = plt.figure(figsize=(11, 5.5))
        
        # Subplot 1: Superficie Combinada 3D
        ax1 = fig.add_subplot(121, projection='3d')
        superficie = ax1.plot_surface(X, Y, Z_total, cmap='inferno', edgecolor='none', alpha=0.8)
        ax1.set_title('Riesgo Total Combinado (P_total)', fontsize=10)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        fig.colorbar(superficie, ax=ax1, shrink=0.5, aspect=10)
        
        # Subplot 2: Curvas de Nivel Deformadas por la Topografía
        ax2 = fig.add_subplot(122)
        curvas = ax2.contour(X, Y, Z_total, levels=14, cmap='inferno')
        ax2.clabel(curvas, inline=True, fontsize=8)
        ax2.plot(x0, y0, 'ro', label=f'Foco ({x0}, {y0})')
        ax2.set_title('Curvas de Nivel Topográficas', fontsize=10)
        ax2.grid(True, linestyle='--', alpha=0.5)
        ax2.legend()
        
        fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.panel_graficos)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppIncendio(root)
    root.mainloop()