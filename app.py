import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =====================================================================
# 1. CONFIGURACIÓN DE PARÁMETROS DEL MODELO (Modifica estos valores aquí)
# =====================================================================
# Parámetros del foco inicial (Ecuación del PDF)
A = 12.0       # Intensidad inicial del incendio (A > 0) [cite: 54]
k = 15.0       # Dispersión espacial del riesgo (k > 0) [cite: 55]
x0 = 0.0       # Coordenada X del foco inicial (x0) [cite: 50]
y0 = 0.0       # Coordenada Y del foco inicial (y0) [cite: 50]

# Parámetros del terreno S(x,y)
alpha = 1.5    # Influencia de la característica sobre la propagación (alpha > 0) [cite: 65]
tipo_terreno = "Valle/Colina"  # Opciones: "Pendiente Lineal", "Valle/Colina", "Irregular"

# Punto específico de la región para calcular la linealización/derivadas locales
eval_x = 2.0
eval_y = 2.0

# =====================================================================
# 2. DEFINICIÓN DE FUNCIONES MATEMÁTICAS
# =====================================================================

# Función S(x, y) que representa la topografía o densidad de vegetación [cite: 56, 66]
def S(X, Y, tipo):
    if tipo == "Pendiente Lineal":
        return 0.4 * X + 0.2 * Y
    elif tipo == "Valle/Colina":
        return 4.0 * np.exp(-(X**2 + Y**2) / 12)
    else:  # Terreno Irregular (Ondulado)
        return np.sin(X) * np.cos(Y)

# Función principal de riesgo P(x, y) dada en el PDF 
def calcular_riesgo(X, Y, A, k, x0, y0, alpha, tipo_s):
    termino_foco = A * np.exp(-((X - x0)**2 + (Y - y0)**2) / k)
    termino_terreno = alpha * S(X, Y, tipo_s)
    return termino_foco + termino_terreno

# =====================================================================
# 3. PROCESAMIENTO MATEMÁTICO Y DE LA MALLA
# =====================================================================

# Definición de la región bidimensional R [-10, 10] x [-10, 10] [cite: 42]
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

# Calcular la superficie de riesgo P(x, y) [cite: 47, 78]
P = calcular_riesgo(X, Y, A, k, x0, y0, alpha, tipo_terreno)

# Cálculo numérico de las Derivadas Parciales (dP/dx, dP/dy) [cite: 83]
dPy, dPx = np.gradient(P, y, x) 

# Búsqueda de índices para la evaluación del punto específico en la terminal
idx_x = (np.abs(x - eval_x)).argmin()
idx_y = (np.abs(y - eval_y)).argmin()

valor_p = P[idx_y, idx_x]
grad_x = dPx[idx_y, idx_x]
grad_y = dPy[idx_y, idx_x]
magnitud_grad = np.sqrt(grad_x**2 + grad_y**2)

# Imprimir el análisis matemático en la terminal (Consola)
print("="*60)
print("📊 INFORME MATEMÁTICO DEL MODELO DE PROPAGACIÓN")
print("="*60)
print(f"Punto evaluado de control: ({eval_x}, {eval_y})")
print(f"• Nivel de Riesgo Local P(x,y): {valor_p:.4f}")
print(f"• Derivada Parcial ∂P/∂x: {grad_x:.4f}")
print(f"• Derivada Parcial ∂P/∂y: {grad_y:.4f}")
print(f"• Magnitud del Vector Gradiente ||∇P||: {magnitud_grad:.4f}")
print("-"*60)
print(f"💡 INTERPRETACIÓN FÍSICA: En la posición ({eval_x}, {eval_y}), el incendio")
print(f"tiende a propagarse con máxima velocidad hacia el vector [{grad_x:.3f}, {grad_y:.3f}].")
print("="*60)

# =====================================================================
# 4. GRÁFICOS Y VISUALIZACIÓN (Matplotlib estándar)
# =====================================================================

# Crear una figura con dos paneles (2D y 3D)
fig = plt.figure(figsize=(14, 6))

# --- GRÁFICO 1: Mapa de Riesgo 2D, Curvas de Nivel y Gradientes ---
ax1 = fig.add_subplot(121)
# Curvas de nivel rellenas (Mapas de riesgo) [cite: 82]
cp = ax1.contourf(X, Y, P, cmap="YlOrRd", levels=15)
fig.colorbar(cp, ax=ax1, label="Nivel de Riesgo P(x,y)")

# Dibujar las líneas de contorno específicas [cite: 79]
lineas_nivel = ax1.contour(X, Y, P, colors='black', linewidths=0.5, levels=10)
ax1.clabel(lineas_nivel, inline=True, fontsize=8)

# Campos vectorialimport numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# =====================================================================
# 1. CONFIGURACIÓN DE PARÁMETROS DEL MODELO (Modifica estos valores aquí)
# =====================================================================
# Parámetros del foco inicial (Ecuación del PDF)
A = 12.0       # Intensidad inicial del incendio (A > 0) [cite: 54]
k = 15.0       # Dispersión espacial del riesgo (k > 0) [cite: 55]
x0 = 0.0       # Coordenada X del foco inicial (x0) [cite: 50]
y0 = 0.0       # Coordenada Y del foco inicial (y0) [cite: 50]

# Parámetros del terreno S(x,y)
alpha = 1.5    # Influencia de la característica sobre la propagación (alpha > 0) [cite: 65]
tipo_terreno = "Valle/Colina"  # Opciones: "Pendiente Lineal", "Valle/Colina", "Irregular"

# Punto específico de la región para calcular la linealización/derivadas locales
eval_x = 2.0
eval_y = 2.0

# =====================================================================
# 2. DEFINICIÓN DE FUNCIONES MATEMÁTICAS
# =====================================================================

# Función S(x, y) que representa la topografía o densidad de vegetación [cite: 56, 66]
def S(X, Y, tipo):
    if tipo == "Pendiente Lineal":
        return 0.4 * X + 0.2 * Y
    elif tipo == "Valle/Colina":
        return 4.0 * np.exp(-(X**2 + Y**2) / 12)
    else:  # Terreno Irregular (Ondulado)
        return np.sin(X) * np.cos(Y)

# Función principal de riesgo P(x, y) dada en el PDF 
def calcular_riesgo(X, Y, A, k, x0, y0, alpha, tipo_s):
    termino_foco = A * np.exp(-((X - x0)**2 + (Y - y0)**2) / k)
    termino_terreno = alpha * S(X, Y, tipo_s)
    return termino_foco + termino_terreno

# =====================================================================
# 3. PROCESAMIENTO MATEMÁTICO Y DE LA MALLA
# =====================================================================

# Definición de la región bidimensional R [-10, 10] x [-10, 10] [cite: 42]
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

# Calcular la superficie de riesgo P(x, y) [cite: 47, 78]
P = calcular_riesgo(X, Y, A, k, x0, y0, alpha, tipo_terreno)

# Cálculo numérico de las Derivadas Parciales (dP/dx, dP/dy) [cite: 83]
dPy, dPx = np.gradient(P, y, x) 

# Búsqueda de índices para la evaluación del punto específico en la terminal
idx_x = (np.abs(x - eval_x)).argmin()
idx_y = (np.abs(y - eval_y)).argmin()

valor_p = P[idx_y, idx_x]
grad_x = dPx[idx_y, idx_x]
grad_y = dPy[idx_y, idx_x]
magnitud_grad = np.sqrt(grad_x**2 + grad_y**2)

# Imprimir el análisis matemático en la terminal (Consola)
print("="*60)
print("📊 INFORME MATEMÁTICO DEL MODELO DE PROPAGACIÓN")
print("="*60)
print(f"Punto evaluado de control: ({eval_x}, {eval_y})")
print(f"• Nivel de Riesgo Local P(x,y): {valor_p:.4f}")
print(f"• Derivada Parcial ∂P/∂x: {grad_x:.4f}")
print(f"• Derivada Parcial ∂P/∂y: {grad_y:.4f}")
print(f"• Magnitud del Vector Gradiente ||∇P||: {magnitud_grad:.4f}")
print("-"*60)
print(f"💡 INTERPRETACIÓN FÍSICA: En la posición ({eval_x}, {eval_y}), el incendio")
print(f"tiende a propagarse con máxima velocidad hacia el vector [{grad_x:.3f}, {grad_y:.3f}].")
print("="*60)

# =====================================================================
# 4. GRÁFICOS Y VISUALIZACIÓN (Matplotlib estándar)
# =====================================================================

# Crear una figura con dos paneles (2D y 3D)
fig = plt.figure(figsize=(14, 6))

# --- GRÁFICO 1: Mapa de Riesgo 2D, Curvas de Nivel y Gradientes ---
ax1 = fig.add_subplot(121)
# Curvas de nivel rellenas (Mapas de riesgo) [cite: 82]
cp = ax1.contourf(X, Y, P, cmap="YlOrRd", levels=15)
fig.colorbar(cp, ax=ax1, label="Nivel de Riesgo P(x,y)")

# Dibujar las líneas de contorno específicas [cite: 79]
lineas_nivel = ax1.contour(X, Y, P, colors='black', linewidths=0.5, levels=10)
ax1.clabel(lineas_nivel, inline=True, fontsize=8)

# Campos vectoriales: Campo de vectores Gradiente (Quiver) [cite: 91]
paso = 5  # Saltar puntos para evitar que se saturen las flechas
ax1.quiver(X[::paso, ::paso], Y[::paso, ::paso], 
           dPx[::paso, ::paso], dPy[::paso, ::paso], 
           color='blue', alpha=0.5, scale=15, label="Gradiente ∇P")

# Marcar el foco del incendio y el punto evaluado [cite: 114]
ax1.plot(x0, y0, 'ro', markersize=8, label="Foco Inicial")
ax1.plot(eval_x, eval_y, 'go', markersize=6, label=f"Punto Evaluado ({eval_x},{eval_y})")

ax1.set_title("🗺️ Curvas de Nivel y Campo de Gradientes (2D)")
ax1.set_xlabel("Eje X (Terreno)")
ax1.set_ylabel("Eje Y (Terreno)")
ax1.legend(loc="upper right")
ax1.grid(True, linestyle="--", alpha=0.5)

# --- GRÁFICO 2: Superficie de Riesgo 3D ---
ax2 = fig.add_subplot(122, projection='3d')
# Graficar la superficie multivariable 
surf = ax2.plot_surface(X, Y, P, cmap="YlOrRd", edgecolor='none', alpha=0.85)
fig.colorbar(surf, ax=ax2, shrink=0.5, aspect=7, label="Riesgo")

ax2.set_title("⛰️ Superficie del Modelo de Riesgo (3D)")
ax2.set_xlabel("Eje X")
ax2.set_ylabel("Eje Y")
ax2.set_zlabel("Riesgo P(x,y)")
ax2.view_init(elev=35, azim=215) # Ángulo de visión inicial ajustable

# Mostrar las ventanas de los gráficos en pantalla
plt.tight_layout()
plt.show()

# Marcar el foco del incendio y el punto evaluado [cite: 114]
ax1.plot(x0, y0, 'ro', markersize=8, label="Foco Inicial")
ax1.plot(eval_x, eval_y, 'go', markersize=6, label=f"Punto Evaluado ({eval_x},{eval_y})")

ax1.set_title("🗺️ Curvas de Nivel y Campo de Gradientes (2D)")
ax1.set_xlabel("Eje X (Terreno)")
ax1.set_ylabel("Eje Y (Terreno)")
ax1.legend(loc="upper right")
ax1.grid(True, linestyle="--", alpha=0.5)

# --- GRÁFICO 2: Superficie de Riesgo 3D ---
ax2 = fig.add_subplot(122, projection='3d')
# Graficar la superficie multivariable 
surf = ax2.plot_surface(X, Y, P, cmap="YlOrRd", edgecolor='none', alpha=0.85)
fig.colorbar(surf, ax=ax2, shrink=0.5, aspect=7, label="Riesgo")

ax2.set_title("⛰️ Superficie del Modelo de Riesgo (3D)")
ax2.set_xlabel("Eje X")
ax2.set_ylabel("Eje Y")
ax2.set_zlabel("Riesgo P(x,y)")
ax2.view_init(elev=35, azim=215) # Ángulo de visión inicial ajustable

# Mostrar las ventanas de los gráficos en pantalla
plt.tight_layout()
plt.show()