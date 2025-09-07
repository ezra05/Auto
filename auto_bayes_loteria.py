import os
import re
import time
from collections import Counter
import math

# Descargar datos con curl (Termux)
def descargar_datos(loteria):
    urls = {
        'newyork': 'URL_DE_DATOS_NEW_YORK.csv',
        'florida': 'URL_DE_DATOS_FLORIDA.csv',
        'ganamas': 'URL_DE_DATOS_GANAMAS.csv',
        'dominicana': 'URL_DE_DATOS_RPDOMINICANA.csv',
        'powerball': 'URL_DE_DATOS_POWERBALL.csv',
        'megamillion': 'URL_DE_DATOS_MEGAMILLION.csv'
    }
    if loteria in urls:
        archivo = f"{loteria}.csv"
        print(f"[INFO] Descargando datos para {loteria}...")
        os.system(f"curl -s -o {archivo} {urls[loteria]}")
        return archivo
    else:
        print("[ERROR] Lotería no soportada.")
        return None

# Leer datos CSV sin librerías externas
def leer_datos_csv(archivo):
    numeros = []
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                if re.match(r'^\d', linea):
                    nums = re.findall(r'\d+', linea)
                    numeros.append(list(map(int, nums)))
    except Exception as e:
        print(f"[ERROR] No pudo leer {archivo}: {e}")
    return numeros

# Bayes manual avanzado con suavizado laplace
def bayesiano_avanzado(historico, total_num):
    prior = {i: 1/total_num for i in range(1, total_num+1)}
    freq = Counter()
    for res in historico:
        freq.update(res)
    total = sum(freq.values()) or 1
    alfa = 1 # suavizado

    posterior = {}
    for num in prior:
        likelihood = (freq[num] + alfa) / (total + alfa*total_num)
        posterior[num] = likelihood * prior[num]

    suma = sum(posterior.values())
    for num in posterior:
        posterior[num] /= suma
    return posterior

# Detección fractal y Mandelbrot sencilla
def mandelbrot_patrones(datos, max_iter=20):
    patrones = Counter()
    for resultado in datos:
        for num in resultado:
            c = complex(math.cos(num), math.sin(num))
            z = 0j
            i = 0
            while abs(z) < 2 and i < max_iter:
                z = z*z + c
                i += 1
            patrones[i] += 1
    return patrones

def graficar(probabilidades, titulo="Probabilidades", top=10):
    print(f"\n=== {titulo} ===")
    ordenado = sorted(probabilidades.items(), key=lambda x: x[1], reverse=True)[:top]
    max_val = ordenado[0][1] if ordenado else 0
    for num, val in ordenado:
        barras = int((val / max_val) * 40) if max_val > 0 else 0
        print(f"{num:2d} | {'█' * barras} {val:.4f}")

def graficar_mandelbrot(patrones):
    print("\n=== Patrón Mandelbrot simplificado ===")
    total = sum(patrones.values()) or 1
    for k, v in sorted(patrones.items()):
        barras = int((v / total) * 40)
        print(f"Iter {k:2d}: {'█' * barras} {v}")

def analizar_loteria(loteria, total_numeros):
    archivo = descargar_datos(loteria)
    if archivo is None:
        return
    datos = leer_datos_csv(archivo)
    if not datos:
        print(f"[WARNING] Sin datos para {loteria}")
        return

    posterior = bayesiano_avanzado(datos, total_numeros)
    mandelbrot_p = mandelbrot_patrones(datos)

    print(f"\n----- {loteria.upper()} -----")
    graficar(posterior, f"Probabilidades Bayes para {loteria}")
    graficar_mandelbrot(mandelbrot_p)

    recomendados = sorted(posterior, key=posterior.get, reverse=True)[:6]
    print(f"\nNúmeros recomendados para jugar en {loteria}: {recomendados}")
    print("-" * 60)

def automatizar_predicciones(intervalo_horas=24):
    loterias = {
        'newyork': 50,
        'florida': 50,
        'ganamas': 50,
        'dominicana': 50,
        'powerball': 69,
        'megamillion': 70
    }

    while True:
        print("\n*** Comenzando ciclo de predicciones ***\n")
        for lot, max_num in loterias.items():
            analizar_loteria(lot, max_num)
        print(f"\nEsperando {intervalo_horas} horas para siguiente predicción...")
        time.sleep(intervalo_horas * 3600)

if __name__ == "__main__":
    # Ejecutar automatización con intervalo de 24 horas (ajustable)
    automatizar_predicciones(intervalo_horas=24)
