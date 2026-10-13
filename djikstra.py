# VERSIÓN MEJORADA
# - Recuperar estaciones cerradas
# - Marca visual de transbordo
# - Coordenadas modificadas para que R1 pase por arriba y luego baje
# - Click izquierdo = ruta
# - Click derecho = cerrar estación
# - Botón recuperar red

import tkinter as tk
from heapq import heappush, heappop
import copy

# ==================================================
# GRAFO ORIGINAL
# ==================================================

grafo_base = {
    "Castelldefels": [("Gavà", "R2")],
    "Gavà": [("Castelldefels", "R2"), ("Viladecans", "R2")],
    "Viladecans": [("Gavà", "R2"), ("El Prat", "R2")],
    "El Prat": [("Viladecans", "R2"), ("Bellvitge", "R2")],
    "Bellvitge": [("El Prat", "R2"), ("Sants", "R2")],
    "Passeig de Gràcia": [("Sants", "R2"), ("Clot", "R2")],

    "Sants": [
        ("Bellvitge", "R2"),
        ("Hospitalet", "R1"),
        ("Plaça Catalunya", "R1"),
        ("Passeig de Gràcia", "R2")
    ],

    "Clot": [
        ("Arc de Triomf", "R1"),
        ("Passeig de Gràcia", "R2")
    ],

    "Plaça Catalunya": [
        ("Sants", "R1"),
        ("Arc de Triomf", "R1")
    ],

    "Arc de Triomf": [
        ("Plaça Catalunya", "R1"),
        ("Clot", "R1")
    ],

    "Hospitalet": [
        ("Cornellà", "R1"),
        ("Sants", "R1")
    ],

    "Cornellà": [
        ("Hospitalet", "R1"),
        ("Sant Joan Despí", "R1")
    ],

    "Sant Joan Despí": [
        ("Cornellà", "R1"),
        ("Sant Feliu", "R1")
    ],

    "Sant Feliu": [
        ("Sant Joan Despí", "R1"),
        ("Molins de Rei", "R1")
    ],

    "Molins de Rei": [
        ("Sant Feliu", "R1")
    ]
}

grafo = copy.deepcopy(grafo_base)

# ==================================================
# NUEVAS COORDENADAS
# ==================================================

pos = {
    # R2 verde
    "Castelldefels": (80, 450),
    "Gavà": (150, 410),
    "Viladecans": (240, 360),
    "El Prat": (340, 320),
    "Bellvitge": (450, 280),
    "Sants": (560, 240),
    "Passeig de Gràcia": (700, 220),
    "Clot": (830, 260),

    # R1 azul sube por arriba y baja
    "Hospitalet": (470, 370),
    "Cornellà": (360, 450),
    "Sant Joan Despí": (260, 540),
    "Sant Feliu": (170, 620),
    "Molins de Rei": (90, 700),

    "Plaça Catalunya": (700, 110),
    "Arc de Triomf": (830, 150)
}

# ==================================================
# DIJKSTRA
# ==================================================

def dijkstra(grafo, inicio, destino):
    cola = []
    heappush(cola, (0, inicio, None, [inicio], []))
    visitados = {}

    while cola:
        coste, nodo, linea_actual, camino, cambios = heappop(cola)

        estado = (nodo, linea_actual)

        if estado in visitados and visitados[estado] <= coste:
            continue

        visitados[estado] = coste

        if nodo == destino:
            return coste, camino, cambios

        for vecino, linea in grafo.get(nodo, []):

            nuevo_coste = coste + 1
            nuevos_cambios = list(cambios)

            if linea_actual is not None and linea != linea_actual:
                nuevo_coste += 3
                nuevos_cambios.append(nodo)

            heappush(
                cola,
                (
                    nuevo_coste,
                    vecino,
                    linea,
                    camino + [vecino],
                    nuevos_cambios
                )
            )

    return None, None, None


# ==================================================
# VENTANA
# ==================================================

ventana = tk.Tk()
ventana.title("Simulador Rodalies")
ventana.geometry("1100x820")

canvas = tk.Canvas(ventana, width=1100, height=740, bg="white")
canvas.pack()

info = tk.Label(
    ventana,
    text="Izq: Ruta | Der: Cerrar estación",
    font=("Arial", 12)
)
info.pack()

# ==================================================
# VARIABLES
# ==================================================

origen = None
destino = None
circulos = {}
ruta_ids = []
cerradas = set()

# ==================================================
# COLORES
# ==================================================

def color_linea(l):
    return "#7ec8ff" if l == "R1" else "green"


# ==================================================
# DIBUJAR
# ==================================================

def dibujar():
    canvas.delete("all")
    circulos.clear()

    hechas = set()

    for a in grafo:
        for b, linea in grafo[a]:

            if (b, a) in hechas:
                continue

            x1, y1 = pos[a]
            x2, y2 = pos[b]

            canvas.create_line(
                x1, y1, x2, y2,
                fill=color_linea(linea),
                width=5
            )

            hechas.add((a, b))

    for est, (x, y) in pos.items():

        color = "gray" if est in cerradas else "white"

        c = canvas.create_oval(
            x-12, y-12, x+12, y+12,
            fill=color,
            outline="black",
            width=2
        )

        circulos[est] = c

        canvas.create_text(
            x, y-18,
            text=est,
            font=("Arial", 9)
        )

        canvas.tag_bind(c, "<Button-1>",
                        lambda e, n=est: click_izq(n))

        canvas.tag_bind(c, "<Button-3>",
                        lambda e, n=est: click_der(n))

        if est in cerradas:
            cruz_roja(x, y)


def cruz_roja(x, y):
    canvas.create_line(x-14, y-14, x+14, y+14,
                       fill="red", width=3)
    canvas.create_line(x-14, y+14, x+14, y-14,
                       fill="red", width=3)


# ==================================================
# CLICK IZQ
# ==================================================

def click_izq(est):
    global origen, destino

    if est in cerradas:
        return

    if origen is None:
        origen = est
        canvas.itemconfig(circulos[est], fill="gold")
        info.config(text=f"Origen: {est}")

    elif destino is None and est != origen:
        destino = est
        canvas.itemconfig(circulos[est], fill="red")
        calcular()

    else:
        reset_ruta()
        origen = est
        destino = None
        canvas.itemconfig(circulos[est], fill="gold")


# ==================================================
# CLICK DER
# ==================================================

def click_der(est):
    if est in cerradas:
        return

    cerradas.add(est)

    for vecino, _ in list(grafo[est]):
        grafo[vecino] = [(v, l) for v, l in grafo[vecino] if v != est]

    grafo[est] = []

    dibujar()
    reset_ruta()
    info.config(text=f"Estación cerrada: {est}")


# ==================================================
# CALCULAR
# ==================================================

def calcular():
    coste, camino, cambios = dijkstra(grafo, origen, destino)

    if camino is None:
        info.config(text="No hay ruta")
        return

    marcar_ruta(camino, cambios)
    info.config(text=f"Ruta encontrada | Coste {coste}")


# ==================================================
# MARCAR RUTA
# ==================================================

def marcar_ruta(camino, cambios):

    for i in range(len(camino)-1):
        a = camino[i]
        b = camino[i+1]

        x1, y1 = pos[a]
        x2, y2 = pos[b]

        rid = canvas.create_line(
            x1, y1, x2, y2,
            fill="orange",
            width=9
        )

        ruta_ids.append(rid)

    for est in camino:
        if est not in (origen, destino):
            canvas.itemconfig(circulos[est], fill="orange")

    # marcar transbordos
    for est in cambios:
        x, y = pos[est]

        rid = canvas.create_text(
            x,
            y+26,
            text="TRANSBORDO",
            fill="red",
            font=("Arial", 8, "bold")
        )

        ruta_ids.append(rid)


# ==================================================
# RESET RUTA
# ==================================================

def reset_ruta():
    global origen, destino

    origen = None
    destino = None

    dibujar()


# ==================================================
# RECUPERAR RED
# ==================================================

def recuperar():
    global grafo, cerradas, origen, destino

    grafo = copy.deepcopy(grafo_base)
    cerradas = set()
    origen = None
    destino = None

    dibujar()
    info.config(text="Red restaurada")


# ==================================================
# BOTONES
# ==================================================

frame = tk.Frame(ventana)
frame.pack(pady=6)

tk.Button(
    frame,
    text="Reiniciar Ruta",
    command=reset_ruta,
    width=18
).grid(row=0, column=0, padx=5)

tk.Button(
    frame,
    text="Recuperar Estaciones",
    command=recuperar,
    width=18
).grid(row=0, column=1, padx=5)


# ==================================================
# MAIN
# ==================================================

dibujar()
ventana.mainloop()