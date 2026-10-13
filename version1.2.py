import flet as ft
import flet.canvas as cv
from flet import Colors, Paint, PaintingStyle
from heapq import heappush, heappop
import copy
import ssl
import os
import math

if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

pos = {
    # R2
    "Aeroport": (300, 680),
    "Castelldefels":    (90, 650),
    "Gavà":             (160, 650),
    "Viladecans":       (230, 650),
    "El Prat":          (300, 650),
    "Bellvitge":        (370, 650),
    "Sant Andreu":      (750, 560),
    "Montcada i Reixac":(790, 520),
    "La Llagosta":      (830, 480),
    "Mollet-Sant Fost": (870, 480),
    "Montmeló":         (910, 480),
    "Granollers-Centre":(950, 480),
    # Nudo central
    "Sants":            (500, 600),
    "Passeig de Gràcia":(550, 600),
    "Clot":             (710, 600),

    # R1 oeste
    "Hospitalet":       (450, 600),
    "Cornellà":         (400, 575),
    "Sant Joan Despí":  (370, 555),
    "Sant Feliu":       (370, 525),
    "Molins de Rei":    (370, 495),
    "El Papiol":        (370, 435),
    "Castellbisbal":    (350, 405),
    "Martorell":        (320, 405),
    "Rubí":             (380, 405),
    "Sant Cugat":       (520, 405),
    "Cerdanyola Universitat":   (600, 405),
    "Santa Perpètua de Mogoda":       (870, 405),
 
    # R1 este
    "Plaça Catalunya":      (550, 620),
    "Arc de Triomf":        (610, 655),
    "La Sagrera-Meridiana": (710, 550),
    "Fabra i Puig":         (740, 520),
    "Torre Baró-Vallbona":  (770, 490),
    "Montcada Bifurcació":  (800, 460),
    
    "Montcada-Manresa":     (770, 430),
    
    #R3
    "Montcada-Ripollet":    (830, 430),
    "La Florida":           (880, 300),
    "Mollet-Santa Rosa":    (880, 250)
}

grafo_base = {
    "Aeroport": [("El Prat", "R2N")],
    # R2
    "Castelldefels":    [("Gavà", "R2")],
    "Gavà":             [("Castelldefels", "R2"), ("Viladecans", "R2")],
    "Viladecans":       [("Gavà", "R2"), ("El Prat", "R2")],
    "El Prat":          [("Viladecans", "R2"), ("Bellvitge", "R2"),
                         ("Aeroport", "R2N"), ("Bellvitge", "R2N")],
    "Bellvitge":        [("El Prat", "R2"), ("Sants", "R2"),
                         ("El Prat", "R2N"), ("Sants", "R2N")],
    "Sants":            [("Bellvitge", "R2"), ("Passeig de Gràcia", "R2"),
                         ("Bellvitge", "R2N"), ("Passeig de Gràcia", "R2N"),
                         ("Hospitalet", "R1"), ("Plaça Catalunya", "R1"),
                         ("Hospitalet", "R3"), ("Plaça Catalunya", "R3"),
                         ("Hospitalet", "R4"), ("Plaça Catalunya", "R4")],
    "Passeig de Gràcia":[("Sants", "R2"), ("Clot", "R2"),
                         ("Sants", "R2N"), ("Clot", "R2N")],
    "Clot":             [("Passeig de Gràcia", "R2"), ("Sant Andreu", "R2"),
                         ("Arc de Triomf", "R1"),
                         ("Passeig de Gràcia", "R2N"), ("Sant Andreu", "R2N")],
    "Sant Andreu":      [("Montcada i Reixac", "R2"), ("Clot", "R2"),
                         ("Montcada i Reixac", "R2N"), ("Clot", "R2N")],
    "Montcada i Reixac":[("La Llagosta", "R2"), ("Sant Andreu", "R2"),
                         ("La Llagosta", "R2N"), ("Sant Andreu", "R2N")],
    "La Llagosta":      [("Montcada i Reixac", "R2"), ("Mollet-Sant Fost", "R2"),
                         ("Montcada i Reixac", "R2N"), ("Mollet-Sant Fost", "R2N")],
    "Mollet-Sant Fost": [("La Llagosta", "R2"), ("Montmeló", "R2"),
                         ("La Llagosta", "R2N"), ("Montmeló", "R2N"),
                         ("Santa Perpètua de Mogoda", "R8"), ("Montmeló", "R8")],
    "Montmeló":         [("Granollers-Centre", "R2"), ("Mollet-Sant Fost", "R2"),
                         ("Granollers-Centre", "R2N"), ("Mollet-Sant Fost", "R2N"),
                         ("Granollers-Centre", "R8"), ("Mollet-Sant Fost", "R8")],
    "Granollers-Centre":[("Montmeló", "R2"),
                        ("Montmeló", "R2N"),
                        ("Montmeló", "R8")],
    # R1 
    "Santa Perpètua de Mogoda": [("Mollet-Sant Fost", "R8"),
                                ("Cerdanyola Universitat", "R8")],
    "Cerdanyola Universitat": [("Sant Cugat", "R8"),
                              ("Santa Perpètua de Mogoda", "R8")],
    "Sant Cugat":       [("Rubí", "R8"),
                        ("Cerdanyola Universitat", "R8")],
    "Rubí":             [("Castellbisbal", "R8"),
                         ("Sant Cugat", "R8")],
    "Martorell":        [("Castellbisbal", "R4"),
                         ("Castellbisbal", "R8")],
    "Castellbisbal":    [("Martorell", "R4"), ("El Papiol", "R4"),
                         ("Martorell", "R8"), ("Rubí", "R8")],
    "El Papiol":        [("Molins de Rei", "R4"), ("Castellbisbal", "R4")],
    "Molins de Rei":    [("Sant Feliu", "R1"),
                         ("Sant Feliu", "R4"), ("El Papiol", "R4")],
    "Sant Feliu":       [("Sant Joan Despí", "R1"), ("Molins de Rei", "R1"),
                         ("Sant Joan Despí", "R4"), ("Molins de Rei", "R4")],
    "Sant Joan Despí":  [("Cornellà", "R1"), ("Sant Feliu", "R1"),
                         ("Cornellà", "R4"), ("Sant Feliu", "R4")],
    "Cornellà":         [("Hospitalet", "R1"), ("Sant Joan Despí", "R1"),
                         ("Hospitalet", "R4"), ("Sant Joan Despí", "R4")],
    # R1 + R3 + R4
    "Hospitalet":       [("Sants", "R1"), ("Cornellà", "R1"),
                         ("Sants", "R3"),
                         ("Sants", "R4"), ("Cornellà", "R4")],    
    "Plaça Catalunya":  [("Sants", "R1"), ("Arc de Triomf", "R1"),
                         ("Sants", "R3"), ("Arc de Triomf", "R3"),
                         ("Sants", "R4"), ("Arc de Triomf", "R4")],
    "Arc de Triomf":    [("Plaça Catalunya", "R1"), ("Clot", "R1"),
                         ("Plaça Catalunya", "R3"), ("La Sagrera-Meridiana", "R3"),
                         ("Plaça Catalunya", "R4"), ("La Sagrera-Meridiana", "R4")],
    "La Sagrera-Meridiana": [("Arc de Triomf", "R3"), ("Fabra i Puig", "R3"),
                                       ("Arc de Triomf", "R4"), ("Fabra i Puig", "R4")],
    "Fabra i Puig": [("La Sagrera-Meridiana", "R3"), ("Torre Baró | Vallbona", "R3"),
                               ("La Sagrera-Meridiana", "R4"), ("Torre Baró | Vallbona", "R4")],
    "Torre Baró-Vallbona": [("Fabra i Puig", "R3"), ("Montcada Bifurcació", "R3"),
                                        ("Fabra i Puig", "R4"), ("Montcada Bifurcació", "R4")],
    "Montcada Bifurcació": [("Torre Baró-Vallbona", "R3"), ("Montcada-Ripollet", "R3"),
                            ("Torre Baró-Vallbona", "R4"), ("Montcada-Manresa", "R4")],
    
    "Montcada-Manresa": [("Montcada Bifurcació", "R4")],
    #R3 a partir de Montcada-Ripollet
    "Montcada-Ripollet":[("Montcada Bifurcació", "R3"), ("La Florida", "R3")],
    "La Florida":       [("Montcada-Ripollet", "R3"), ("Mollet-Santa Rosa", "R3")],
    "Mollet-Santa Rosa":[("Parets del Vallés", "R3"), ("La Florida", "R3")],
    "Parets del Vallés":[("Mollet-Santa Rosa", "R3"), ("Granollers-Canovelles", "R3")],
    "Granollers-Canovelles":[("Parets del Vallés", "R3"), ("Les Franqueses", "R3")],
    "Les Franqueses":   [("La Garriga", "R3"), ("Granollers-Canovelles", "R3")],
    "La Garriga":       [("Figaró", "R3"), ("Les Franqueses", "R3")],
    "Figaró":           [("La Garriga", "R3"), ("Sant Martí de Centelles", "R3")],
    "Sant Martí de Centelles":  [("Figaró", "R3"), ("Centelles", "R3")],
    "Centelles":        [("Balenyà-Els Hostalets", "R3"), ("Sant Martí de Centelles", "R3")],
    "Balenyà-Els Hostalets": [("Balenyà-Tona-Seva", "R3"), ("Centelles", "R3")],
    "Balenyà-Tona-Seva":[("Balenyà-Els Hostalets", "R3"), ("Vic", "R3")],
    "Vic":              [("Balenyà-Tona-Seva", "R3"), ("Manlleu", "R3")],
    "Manlleu":          [("Torrelló", "R3"), ("Vic", "R3")],
    "Torrelló":         [("Borgonyà", "R3"), ("Manlleu", "R3")],
    "Borgonyà":         [("Torrelló", "R3"), ("Sant Quirze de Besora", "R3")],
    "Sant Quirze de Besora": [("Borgonyà", "R3")]
                                    
}

COLORES_LINEA = {
    "R1": "#4FC3F7",
    "R2": "#66BB6A",
    "R2N": "#B5ED70",
    "R3": "#F91111",
    "R4": "#FFAF01",
    "R8": "#AE07DC",
}

def dijkstra(actual_grafo, inicio, destino):
    cola = []
    heappush(cola, (0, inicio, None, [inicio], [], []))  # añadimos [] para lineas
    visitados = {}
    while cola:
        coste, nodo, linea_actual, camino, cambios, lineas = heappop(cola)
        estado = (nodo, linea_actual)
        if estado in visitados and visitados[estado] <= coste: continue
        visitados[estado] = coste
        if nodo == destino: return coste, camino, cambios, lineas
        for vecino, linea in actual_grafo.get(nodo, []):
            nuevo_coste = coste + 1
            nuevos_cambios = list(cambios)
            if linea_actual is not None and linea != linea_actual:
                nuevo_coste += 3
                nuevos_cambios.append(nodo)
            heappush(cola, (nuevo_coste, vecino, linea, camino + [vecino], nuevos_cambios, lineas + [linea]))
    return None, None, None, None

def main(page: ft.Page):
    page.title = "Simulador Rodalies TR"
    page.bgcolor = "#1a1c1e"
    page.window_maximized = True

    state = {
        "grafo": copy.deepcopy(grafo_base),
        "origen": None, "destino": None,
        "cerradas": set(), "camino": [], "cambios": [],
        "lineas_camino": []
    }

    cv_mapa = cv.Canvas(expand=True)
    info_text = ft.Text("Selecciona una estación de origen", size=16, color=Colors.WHITE, weight="bold")

    def dibujar_red():
        cv_mapa.shapes.clear()

        # 1. Recopilar todos los tramos y qué líneas pasan por cada uno
        tramos = {}  # (a, b) -> set de líneas
        for a in state["grafo"]:
            for b, linea in state["grafo"][a]:
                key = tuple(sorted([a, b]))
                if key not in tramos:
                    tramos[key] = set()
                tramos[key].add(linea)

        # 2. Dibujar cada tramo con líneas paralelas si hay varias líneas
        OFFSET = 4  # píxeles de separación entre líneas paralelas

        for (a, b), lineas in tramos.items():
            if a not in pos or b not in pos:
                continue
            x1, y1 = pos[a]
            x2, y2 = pos[b]

            
            dx, dy = x2 - x1, y2 - y1
            length = math.sqrt(dx*dx + dy*dy) or 1
            px, py = -dy / length, dx / length
            
            if py > 0 or (py == 0 and px > 0):
                px, py = -px, -py
            lineas_lista = sorted(lineas)  # orden fijo: R1, R2, R3... por nombre
            n = len(lineas_lista)
            offsets = [(i - (n - 1) / 2) * OFFSET for i in range(n)]

            for linea, off in zip(lineas_lista, offsets):
                ox, oy = px * off, py * off

                # Buscar si este tramo+línea está en la ruta y con qué línea
                es_ruta_este_tramo = False
                col_ruta = None
                for i in range(len(state["camino"]) - 1):
                    na, nb = state["camino"][i], state["camino"][i+1]
                    linea_usada = state["lineas_camino"][i]
                    if (na == a and nb == b) or (na == b and nb == a):
                        if linea_usada == linea:
                            es_ruta_este_tramo = True
                            col_ruta = COLORES_LINEA.get(linea_usada, Colors.WHITE)
                            break

                if es_ruta_este_tramo:
                    # Borde blanco exterior
                    cv_mapa.shapes.append(cv.Line(
                        x1 + ox, y1 + oy,
                        x2 + ox, y2 + oy,
                        paint=Paint(color="white", stroke_width=13)
                    ))
                    # Color de la línea encima
                    cv_mapa.shapes.append(cv.Line(
                        x1 + ox, y1 + oy,
                        x2 + ox, y2 + oy,
                        paint=Paint(color=col_ruta, stroke_width=8)
                    ))
                else:
                    cv_mapa.shapes.append(cv.Line(
                        x1 + ox, y1 + oy,
                        x2 + ox, y2 + oy,
                        paint=Paint(color=COLORES_LINEA.get(linea, Colors.WHITE), stroke_width=5)
                    ))

        # 3. Dibujar estaciones encima (igual que antes)
        def angulo_estacion(est):
            vecinos = [v for v, _ in state["grafo"].get(est, []) if v in pos]
            if not vecinos:
                return 0, -1, 18, 0
            x0, y0 = pos[est]
            dx_total, dy_total = 0, 0
            for v in vecinos:
                xv, yv = pos[v]
                dx_total += xv - x0
                dy_total += yv - y0

            # Si más horizontal → arriba. Si más vertical → derecha.
            if abs(dx_total) >= abs(dy_total):
                # arriba: texto centrado encima del nodo
                return 0, -8, 0, -22
            else:
                # derecha: texto a la derecha del nodo
                return 1, 0, 16, -6
        for est, (x, y) in pos.items():
            dot_col = Colors.WHITE
            if est == state["origen"]:     dot_col = Colors.AMBER
            elif est == state["destino"]:  dot_col = Colors.RED
            elif est in state["camino"]:   dot_col = Colors.ORANGE
            elif est in state["cerradas"]: dot_col = Colors.GREY_700

            cv_mapa.shapes.append(cv.Circle(x, y, 9, paint=Paint(color=dot_col, style=PaintingStyle.FILL)))
            cv_mapa.shapes.append(cv.Circle(x, y, 9, paint=Paint(color="#555", stroke_width=2, style=PaintingStyle.STROKE)))

            px, py, ox, oy = angulo_estacion(est)
            cv_mapa.shapes.append(cv.Text(x + ox, y + oy, est, ft.TextStyle(size=10, color=Colors.WHITE)))

            if est in state["cerradas"]:
                cv_mapa.shapes.append(cv.Line(x-7, y-7, x+7, y+7, paint=Paint(color=Colors.RED, stroke_width=3)))
                cv_mapa.shapes.append(cv.Line(x-7, y+7, x+7, y-7, paint=Paint(color=Colors.RED, stroke_width=3)))
            if est in state["cambios"]:
                cv_mapa.shapes.append(cv.Text(x, y+18, "TRANSBORDO",
                    ft.TextStyle(size=9, color=Colors.RED_ACCENT, weight="bold")))

        page.update()

    def on_click_izq(e: ft.TapEvent):
        for est, (x, y) in pos.items():
            if ((e.local_position.x - x)**2 + (e.local_position.y - y)**2)**0.5 < 22:
                if est in state["cerradas"]: return
                if state["origen"] is None:
                    state["origen"] = est
                    info_text.value = f"Origen: {est}. Elige destino."
                elif state["destino"] is None and est != state["origen"]:
                    state["destino"] = est
                    coste, camino, cambios, lineas = dijkstra(state["grafo"], state["origen"], state["destino"])
                    if camino:
                        state["camino"], state["cambios"], state["lineas_camino"] = camino, cambios, lineas
                        paradas = len(camino) - 1
                        if cambios:
                            detalle = ", ".join(cambios)
                            transbordos_txt = f" | {len(cambios)} transbordo{'s' if len(cambios) > 1 else ''} en {detalle}"
                        else:
                            transbordos_txt = " | Sin transbordos"
                        info_text.value = f"✅ {state['origen']} → {state['destino']} | {paradas} paradas{transbordos_txt}"
                    else:
                        info_text.value = "❌ No hay ruta disponible"
                else:
                    state["origen"], state["destino"] = est, None
                    state["camino"], state["cambios"], state["lineas_camino"] = [], [], []
                    info_text.value = f"Origen: {est}. Elige destino."
                dibujar_red()
                return

    def on_click_der(e: ft.TapEvent):
        for est, (x, y) in pos.items():
            if ((e.local_position.x - x)**2 + (e.local_position.y - y)**2)**0.5 < 22:
                if est not in state["cerradas"]:
                    state["cerradas"].add(est)
                    for v in state["grafo"]:
                        state["grafo"][v] = [(d, l) for d, l in state["grafo"][v] if d != est]
                    state["grafo"][est] = []
                    state["camino"] = []
                    info_text.value = f"⛔ {est} cerrada"
                else:
                    state["cerradas"].discard(est)
                    state["grafo"] = copy.deepcopy(grafo_base)
                    for cerrada in state["cerradas"]:
                        for v in state["grafo"]:
                            state["grafo"][v] = [(d, l) for d, l in state["grafo"][v] if d != cerrada]
                        state["grafo"][cerrada] = []
                    info_text.value = f"✅ {est} reabierta"
                dibujar_red()
                return

    def reset_all(e):
        state["grafo"] = copy.deepcopy(grafo_base)
        state["cerradas"].clear()
        state["origen"] = state["destino"] = None
        state["camino"], state["cambios"], state["lineas_camino"] = [], [], []
        info_text.value = "Red reiniciada"
        dibujar_red()

    mapa_interactivo = ft.GestureDetector(
        content=ft.Container(content=cv_mapa, expand=True),
        on_tap_down=on_click_izq,
        on_secondary_tap_down=on_click_der,
    )

    leyenda = ft.Row([
        ft.Text("━ R1", color="#4FC3F7", size=13, weight="bold"),
        ft.Text("━ R2", color="#66BB6A", size=13, weight="bold"),
        ft.Text("━ R2N", color="#B5ED70", size=13, weight="bold"),
        ft.Text("━ R3", color="#F91111", size=13, weight="bold"),
        ft.Text("━ R4", color="#FFAF01", size=13, weight="bold"),
        ft.Text("━ R8", color="#AE07DC", size=13, weight="bold"),

    ], spacing=15)

    controles = ft.Container(
        content=ft.Column([
            ft.Text("SIMULADOR DE RODALIES", size=26, weight="bold", color=Colors.AMBER),
            info_text,
            ft.Row([
                ft.ElevatedButton("Reiniciar", icon="refresh", on_click=reset_all),
                ft.Text("Click izq: seleccionar | Click der: cerrar/reabrir",
                        color=Colors.WHITE60, size=12),
            ]),
            leyenda,
        ], spacing=6),
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        bgcolor="#25282b",
        border_radius=10,
        margin=10,
    )

    page.add(
        ft.Stack([
            mapa_interactivo,
            ft.Column([controles]),
        ], expand=True)
    )
    dibujar_red()

ft.app(target=main)