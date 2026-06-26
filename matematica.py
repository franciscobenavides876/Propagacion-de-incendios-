# =====================================================================
# ARCHIVO: matematica.py
# DESCRIPCIÓN: Módulo de cálculo matemático para el Foco de Incendio.
#              Contiene el modelo exponencial y sus derivadas.
# =====================================================================

import numpy as np

def inicializar_malla(x0, y0, radio_estudio=10, puntos=100):
    x = np.linspace(x0 - radio_estudio, x0 + radio_estudio, puntos)
    y = np.linspace(y0 - radio_estudio, y0 + radio_estudio, puntos)
    X, Y = np.meshgrid(x, y)
    return X, Y

def calcular_riesgo_foco(X, Y, A, k, x0, y0):
    distancia_cuadrado = (X - x0)**2 + (Y - y0)**2
    Z_foco = A * np.exp(-distancia_cuadrado / k)
    return Z_foco

def calcular_derivadas_foco(X, Y, Z_foco, A, k, x0, y0):
    """
    Calcula las derivadas parciales del riesgo respecto a los 
    parámetros dinámicos A (Intensidad) y k (Dispersión).
    """
    distancia_cuadrado = (X - x0)**2 + (Y - y0)**2
    
    # Derivada respecto a A: dF/dA = e^(-((x-x0)^2 + (y-y0)^2) / k)
    dF_dA = np.exp(-distancia_cuadrado / k)
    
    # Derivada respecto a k: dF/dk = F(x,y) * ((x-x0)^2 + (y-y0)^2) / k^2
    dF_dk = Z_foco * (distancia_cuadrado / (k**2))
    
    return dF_dA, dF_dk