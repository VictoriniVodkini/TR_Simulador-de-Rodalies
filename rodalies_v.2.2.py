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
    "Sant Vicenç de Calders": (30, 650),
    "Calafell": (60, 650),
    "Segur de Calafell": (90, 650),
    "Cunit": (120, 650),
    "Cubelles": (150, 650),
    "Vilanova i la Geltrú": (180, 650),
    "Sitges": (210, 650),
    "Garraf": (240, 650),
    "Platja de Castelldefels": (270, 650),
    "Castelldefels": (300, 650),
    "Gavà": (330, 650),
    "Viladecans": (360, 650),
    "El Prat": (390, 650),
    "Bellvitge": (420, 650),
    "Aeroport": (390, 680),
    "Sant Andreu":      (750, 560),
    "Montcada i Reixac":(790, 520),
    "La Llagosta":      (810, 500),
    "Mollet-Sant Fost": (850, 500),
    "Montmeló":         (880, 500),
    "Granollers-Centre":(910, 500),
    "Granollers-Nord":  (940, 500),
    "Cardedeu":         (970, 500),
    "Llinars del Vallés": (1000, 500),
    "Palautordera":     (1030, 500),
    "Sant Celoni":      (1060, 500),
    "Gualba":           (1090, 500),
    "Riells i Viabrea-Bred": (1120, 500),
    "Hostalric":        (1150, 500),
    "Maçanet-Massanes": (1180, 500),
    # Nudo central
    "Sants":            (500, 600),
    "Passeig de Gràcia":(550, 600),
    "Clot":             (710, 600),

    # R1 oeste
    "Hospitalet":       (450, 600),
    "Cornellà":         (400, 550),
    "Sant Joan Despí":  (370, 510),
    "Sant Feliu":       (370, 470),
    "Molins de Rei":    (370, 430),
    "El Papiol":        (370, 390),
    "Castellbisbal":    (370, 350),
    "Martorell":        (330, 350),
    "Rubí":             (420, 350),
    "Sant Cugat":       (520, 350),
    "Cerdanyola Universitat":   (600, 350),
    "Santa Perpètua de Mogoda":       (850, 350),

    # R1 este
    "Plaça Catalunya":      (550, 620),
    "Arc de Triomf":        (610, 655),
    "La Sagrera-Meridiana": (710, 550),
    "Fabra i Puig":         (740, 520),
    "Torre Baró-Vallbona":  (770, 490),
    "Montcada Bifurcació":  (800, 460),

    "Montcada-Manresa":     (770, 430),
    "Montcada i Reixac-Santa Maria": (770, 400),
    "Cerdanyola del Vallès": (770, 370),
    "Barberà del Vallès": (770, 340),
    "Sabadell Sud": (770, 310),
    "Sabadell Centre": (770, 280),
    "Sabadell Nord": (770, 250),
    "Terrassa Est": (770, 220),

    "Terrassa Estació del Nord": (740, 220),
    "Sant Miquel de Gonteres-Viladecavalls": (710, 220),
    "Viladecavalls": (680, 220),
    "Vacarisses-Torreblanca": (650, 220),
    "Vacarisses": (620, 220),
    "Castellbell i el Vilar-Monistrol de Mont": (590, 220),
    "Sant Vicenç de Castellet": (560, 220),
    "Manresa": (530, 220),
    # R3
    "Montcada-Ripollet":    (830, 430),
    "La Florida":           (880, 430),
    "Mollet-Santa Rosa":    (930, 430),

    # R3 norte - rama hacia Vic / Sant Quirze de Besora (COMPLETAR)
    "Parets del Vallés":          (980, 430),
    "Granollers-Canovelles":      (1030, 430),
    "Les Franqueses":             (1080, 430),
    "La Garriga":                 (1100, 415),
    "Figaró":                     (1120, 400),
    "Sant Martí de Centelles":    (1120, 375),
    "Centelles":                  (1120, 350),
    "Balenyà-Els Hostalets":      (1120, 325),
    "Balenyà-Tona-Seva":          (1120, 300),
    "Vic":                        (1120, 275),
    "Manlleu":                    (1120, 250),
    "Torrelló":                   (1120, 225),
    "Borgonyà":                   (1120, 200),
    "Sant Quirze de Besora":      (1120, 175),
    "Sant Adrià de Besòs": (690, 650),
    "Badalona": (740, 650),
    "Montgat": (770, 650),
    "Montgat Nord": (800, 650),
    "El Masnou": (830, 650),
    "Ocata": (860, 650),
    "Premià de Mar": (890, 650),
    "Vilassar de Mar": (920, 650),
    "Cabrera de Mar": (950, 650),
    "Mataró": (980, 650),
    "Sant Andreu de Llavaneres": (1010, 650),
    "Caldes d'Estrac": (1040, 650),
    "Arenys de Mar": (1070, 650),
    "Canet de Mar": (1100, 650),
    "Sant Pol de Mar": (1130, 650),
    "Calella": (1160, 650),
    "Pineda de Mar": (1190, 650),
    "Santa Susanna": (1220, 650),
    "Malgrat de Mar": (1250, 650),
    "Blanes": (1280, 650),
    "Tordera": (1280, 600),
    #R1 - Mataró
}

# Direcciones posibles: "arriba", "abajo", "izquierda", "derecha",
# "arriba_izq", "arriba_der", "abajo_izq", "abajo_der"

etiquetas = {
    # R2 costa
    "Aeroport":          "derecha",
    "Castelldefels":     "arriba",
    "Gavà":              "arriba",
    "Viladecans":        "arriba",
    "El Prat":           "arriba",
    "Bellvitge":         "arriba",

    # R2 norte (Sant Andreu → Granollers-Centre)
    "Sant Andreu":       "derecha",
    "Montcada i Reixac": "derecha",
    "La Llagosta":       "arriba",
    "Mollet-Sant Fost":  "arriba",
    "Montmeló":          "arriba",
    "Granollers-Centre": "arriba",
    "Granollers-Nord":  "arriba",
    "Cardedeu":         "arriba",
    "Llinars del Vallés": "arriba",
    "Palautordera":     "arriba",
    "Sant Celoni":      "arriba",
    "Gualba":           "arriba",
    "Riells i Viabrea-Bred": "arriba",
    "Hostalric":        "arriba",
    "Maçanet-Massanes": "arriba_izq",
    # Nudo central
    "Sants":             "arriba",
    "Passeig de Gràcia": (0,  -30,   0),
    "Clot":              "derecha",

    # R1 oeste
    "Hospitalet":        "arriba",
    "Cornellà":          "derecha",
    "Sant Joan Despí":   "derecha",
    "Sant Feliu":        "derecha",
    "Molins de Rei":     "derecha",
    "El Papiol":         "derecha",
    "Castellbisbal":     "arriba",
    "Martorell":         "arriba",
    "Rubí":              "arriba",
    "Sant Cugat":        "arriba",
    "Cerdanyola Universitat":    "arriba",
    "Santa Perpètua de Mogoda":  "arriba",

    # R1 este
    "Plaça Catalunya":   (-70,  40,   -35),
    "Arc de Triomf":     "abajo",
    "La Sagrera-Meridiana":      "izquierda",
    "Fabra i Puig":               "izquierda",
    "Torre Baró-Vallbona":       "izquierda",
    "Montcada Bifurcació":       "izquierda",
    "Montcada-Manresa":          "izquierda",

    # R3 sur
    "Montcada-Ripollet":         "arriba_izq",
    "La Florida":                "arriba",
    "Mollet-Santa Rosa":         "arriba_izq",

    # R3 norte (Vic / Sant Quirze de Besora)
    "Parets del Vallés":         "arriba_izq",
    "Granollers-Canovelles":     "arriba_izq",
    "Les Franqueses":            "derecha",
    "La Garriga":                "derecha",
    "Figaró":                    "derecha",
    "Sant Martí de Centelles":   "derecha",
    "Centelles":                 "derecha",
    "Balenyà-Els Hostalets":     "derecha",
    "Balenyà-Tona-Seva":         "derecha",
    "Vic":                       "derecha",
    "Manlleu":                   "derecha",
    "Torrelló":                  "derecha",
    "Borgonyà":                  "derecha",
    "Sant Quirze de Besora":     "derecha",

    #R1 - Mataró
}

DIRECCIONES = {
    # nombre: (offset_x, offset_y, angulo_grados, align)
    "arriba":       (0,   -20,   -35, "center"),
    "abajo":        (-30,    7,   0, "center"),
    "izquierda":    (-12,  -13,   0, "right"),
    "derecha":      (12,   -8,   0, "left"),
    "arriba_izq":   (-10, -20,   -35, "right"),
    "arriba_der":   (10,  -20,   -35, "left"),
    "abajo_izq":    (-10,  16,   -35, "right"),
    "abajo_der":    (10,   16,   -35, "left"),
}

def ancho_aproximado_texto(texto, tamano_fuente=10):
    # Estimación: cada carácter ocupa aprox. 0.5 * tamaño de fuente en píxeles
    return len(texto) * tamano_fuente * 0.5

def calcular_etiqueta(est, x, y):
    direccion = etiquetas.get(est, "arriba")

    # Modo manual: tupla (ox, oy) o (ox, oy, angulo)
    if isinstance(direccion, tuple):
        ox, oy, angulo = direccion
        return x + ox, y + oy, angulo, "left"

    # Modo automático: string con dirección
    ox, oy, angulo, align = DIRECCIONES[direccion]
    tx, ty = x + ox, y + oy
    if direccion == "izquierda":
        ancho = ancho_aproximado_texto(est)
        tx -= ancho
    return tx, ty, angulo, align

graf_base = {
    "Aeroport": [("El Prat", "R2N")],

    # R2
    "Sant Vicenç de Calders": [("Calafell", "R2S")],
    "Calafell": [("Sant Vicenç de Calders", "R2S"), ("Segur de Calafell", "R2S")],
    "Segur de Calafell": [("Calafell", "R2S"), ("Cunit", "R2S")],
    "Cunit": [("Segur de Calafell", "R2S"), ("Cubelles", "R2S")],
    "Cubelles": [("Cunit", "R2S"), ("Vilanova i la Geltrú", "R2S")],
    "Vilanova i la Geltrú": [("Cubelles", "R2S"), ("Sitges", "R2S")],
    "Sitges": [("Vilanova i la Geltrú", "R2S"), ("Garraf", "R2S")],
    "Garraf": [("Sitges", "R2S"), ("Platja de Castelldefels", "R2S")],
    "Platja de Castelldefels": [("Garraf", "R2S"), ("Castelldefels", "R2S")],

    "Castelldefels": [
        ("Gavà", "R2"),
        ("Platja de Castelldefels", "R2S"), ("Gavà", "R2S")
    ],

    "Gavà": [
        ("Castelldefels", "R2"), ("Viladecans", "R2"),
        ("Castelldefels", "R2S"), ("Viladecans", "R2S")
    ],

    "Viladecans": [
        ("Gavà", "R2"), ("El Prat", "R2"),
        ("Gavà", "R2S"), ("El Prat", "R2S")
    ],

    "El Prat": [
        ("Viladecans", "R2"), ("Bellvitge", "R2"),
        ("Aeroport", "R2N"), ("Bellvitge", "R2N"),
        ("Viladecans", "R2S"), ("Bellvitge", "R2S")
    ],

    "Bellvitge": [
        ("El Prat", "R2"), ("Sants", "R2"),
        ("El Prat", "R2N"), ("Sants", "R2N"),
        ("El Prat", "R2S"), ("Sants", "R2S")
    ],

    "Sants": [
        ("Bellvitge", "R2"), ("Passeig de Gràcia", "R2"),
        ("Bellvitge", "R2N"), ("Passeig de Gràcia", "R2N"),
        ("Bellvitge", "R2S"), ("Passeig de Gràcia", "R2S"),
        ("Hospitalet", "R1"), ("Plaça Catalunya", "R1"),
        ("Hospitalet", "R3"), ("Plaça Catalunya", "R3"),
        ("Hospitalet", "R4"), ("Plaça Catalunya", "R4")
    ],

    "Passeig de Gràcia": [
        ("Sants", "R2"), ("Clot", "R2"),
        ("Sants", "R2N"), ("Clot", "R2N"),
        ("Sants", "R2S"), ("Clot", "R2S")
    ],

    "Clot": [
        ("Passeig de Gràcia", "R2"), ("Sant Andreu", "R2"),
        ("Arc de Triomf", "R1"),
        ("Passeig de Gràcia", "R2N"), ("Sant Andreu", "R2N")
    ],

    "Sant Andreu": [
        ("Montcada i Reixac", "R2"), ("Clot", "R2"),
        ("Montcada i Reixac", "R2N"), ("Clot", "R2N")
    ],

    "Montcada i Reixac": [
        ("La Llagosta", "R2"), ("Sant Andreu", "R2"),
        ("La Llagosta", "R2N"), ("Sant Andreu", "R2N")
    ],

    "La Llagosta": [
        ("Montcada i Reixac", "R2"), ("Mollet-Sant Fost", "R2"),
        ("Montcada i Reixac", "R2N"), ("Mollet-Sant Fost", "R2N")
    ],

    "Mollet-Sant Fost": [
        ("La Llagosta", "R2"), ("Montmeló", "R2"),
        ("La Llagosta", "R2N"), ("Montmeló", "R2N"),
        ("Santa Perpètua de Mogoda", "R8"), ("Montmeló", "R8")
    ],

    "Montmeló": [
        ("Granollers-Centre", "R2"), ("Mollet-Sant Fost", "R2"),
        ("Granollers-Centre", "R2N"), ("Mollet-Sant Fost", "R2N"),
        ("Granollers-Centre", "R8"), ("Mollet-Sant Fost", "R8")
    ],

    "Granollers-Centre": [
        ("Montmeló", "R2"),
        ("Montmeló", "R2N"), ("Granollers-Nord", "R2N"),
        ("Montmeló", "R8")
    ],

    "Granollers-Nord": [("Granollers-Centre", "R2N"), ("Cardedeu", "R2N")],
    "Cardedeu": [("Granollers-Nord", "R2N"), ("Llinars del Vallés", "R2N")],
    "Llinars del Vallés": [("Palautordera", "R2N"), ("Cardedeu", "R2N")],
    "Palautordera": [("Sant Celoni", "R2N"), ("Llinars del Vallés", "R2N")],
    "Sant Celoni": [("Palautordera", "R2N"), ("Gualba", "R2N")],
    "Gualba": [("Sant Celoni", "R2N"), ("Riells i Viabrea-Bred", "R2N")],
    "Riells i Viabrea-Bred": [("Hostalric", "R2N"), ("Gualba", "R2N")],
    "Hostalric": [("Maçanet-Massanes", "R2N"), ("Riells i Viabrea-Bred", "R2N")],
    "Maçanet-Massanes": [("Tordera", "R1"), ("Hostalric", "R2N")],

    # R8
    "Santa Perpètua de Mogoda": [
        ("Mollet-Sant Fost", "R8"),
        ("Cerdanyola Universitat", "R8")
    ],

    "Cerdanyola Universitat": [
        ("Sant Cugat", "R8"),
        ("Santa Perpètua de Mogoda", "R8"),
        ("Cerdanyola del Vallès", "R7")
    ],

    "Sant Cugat": [("Rubí", "R8"), ("Cerdanyola Universitat", "R8")],
    "Rubí": [("Castellbisbal", "R8"), ("Sant Cugat", "R8")],

    # R4
    "Martorell": [("Castellbisbal", "R4"), ("Castellbisbal", "R8")],

    "Castellbisbal": [
        ("Martorell", "R4"), ("El Papiol", "R4"),
        ("Martorell", "R8"), ("Rubí", "R8")
    ],

    "El Papiol": [("Molins de Rei", "R4"), ("Castellbisbal", "R4")],

    "Molins de Rei": [
        ("Sant Feliu", "R1"),
        ("Sant Feliu", "R4"), ("El Papiol", "R4")
    ],

    "Sant Feliu": [
        ("Sant Joan Despí", "R1"), ("Molins de Rei", "R1"),
        ("Sant Joan Despí", "R4"), ("Molins de Rei", "R4")
    ],

    "Sant Joan Despí": [
        ("Cornellà", "R1"), ("Sant Feliu", "R1"),
        ("Cornellà", "R4"), ("Sant Feliu", "R4")
    ],

    "Cornellà": [
        ("Hospitalet", "R1"), ("Sant Joan Despí", "R1"),
        ("Hospitalet", "R4"), ("Sant Joan Despí", "R4")
    ],

    # R1 + R3 + R4
    "Hospitalet": [
        ("Sants", "R1"), ("Cornellà", "R1"),
        ("Sants", "R3"),
        ("Sants", "R4"), ("Cornellà", "R4")
    ],

    "Plaça Catalunya": [
        ("Sants", "R1"), ("Arc de Triomf", "R1"),
        ("Sants", "R3"), ("Arc de Triomf", "R3"),
        ("Sants", "R4"), ("Arc de Triomf", "R4")
    ],

    "Arc de Triomf": [
        ("Plaça Catalunya", "R1"), ("Clot", "R1"),
        ("Plaça Catalunya", "R3"), ("La Sagrera-Meridiana", "R3"),
        ("Plaça Catalunya", "R4"), ("La Sagrera-Meridiana", "R4")
    ],

    "La Sagrera-Meridiana": [
        ("Arc de Triomf", "R3"), ("Fabra i Puig", "R3"),
        ("Arc de Triomf", "R4"), ("Fabra i Puig", "R4")
    ],

    "Fabra i Puig": [
        ("La Sagrera-Meridiana", "R3"), ("Torre Baró-Vallbona", "R3"),
        ("La Sagrera-Meridiana", "R4"), ("Torre Baró-Vallbona", "R4"),
        ("Torre Baró-Vallbona", "R7")
    ],

    "Torre Baró-Vallbona": [
        ("Fabra i Puig", "R3"), ("Montcada Bifurcació", "R3"),
        ("Fabra i Puig", "R4"), ("Montcada Bifurcació", "R4"),
        ("Fabra i Puig", "R7"), ("Montcada Bifurcació", "R7")
    ],

    "Montcada Bifurcació": [
        ("Torre Baró-Vallbona", "R3"), ("Montcada-Ripollet", "R3"),
        ("Torre Baró-Vallbona", "R4"), ("Montcada-Manresa", "R4"),
        ("Torre Baró-Vallbona", "R7"), ("Montcada-Manresa", "R7")
    ],

    "Montcada-Manresa": [
        ("Montcada Bifurcació", "R4"), ("Montcada i Reixac-Santa Maria", "R4"),
        ("Montcada Bifurcació", "R7"), ("Montcada i Reixac-Santa Maria", "R7")
    ],

    "Montcada i Reixac-Santa Maria": [
        ("Montcada-Manresa", "R4"), ("Cerdanyola del Vallès", "R4"),
        ("Montcada-Manresa", "R7"), ("Cerdanyola del Vallès", "R7")
    ],

    "Cerdanyola del Vallès": [
        ("Montcada i Reixac-Santa Maria", "R4"), ("Barberà del Vallès", "R4"),
        ("Montcada i Reixac-Santa Maria", "R7"), ("Cerdanyola Universitat", "R7")
    ],

    "Barberà del Vallès": [("Cerdanyola del Vallès", "R4"), ("Sabadell Sud", "R4")],
    "Sabadell Sud": [("Barberà del Vallès", "R4"), ("Sabadell Centre", "R4")],
    "Sabadell Centre": [("Sabadell Sud", "R4"), ("Sabadell Nord", "R4")],
    "Sabadell Nord": [("Sabadell Centre", "R4"), ("Terrassa Est", "R4")],
    "Terrassa Est": [("Sabadell Nord", "R4"), ("Terrassa Estació del Nord", "R4")],
    "Terrassa Estació del Nord": [("Terrassa Est", "R4"), ("Sant Miquel de Gonteres-Viladecavalls", "R4")],
    "Sant Miquel de Gonteres-Viladecavalls": [("Terrassa Estació del Nord", "R4"), ("Viladecavalls", "R4")],
    "Viladecavalls": [("Sant Miquel de Gonteres-Viladecavalls", "R4"), ("Vacarisses-Torreblanca", "R4")],
    "Vacarisses-Torreblanca": [("Viladecavalls", "R4"), ("Vacarisses", "R4")],
    "Vacarisses": [("Vacarisses-Torreblanca", "R4"), ("Castellbell i el Vilar-Monistrol de Mont", "R4")],
    "Castellbell i el Vilar-Monistrol de Mont": [("Vacarisses", "R4"), ("Sant Vicenç de Castellet", "R4")],
    "Sant Vicenç de Castellet": [("Castellbell i el Vilar-Monistrol de Mont", "R4"), ("Manresa", "R4")],
    "Manresa": [("Sant Vicenç de Castellet", "R4")],

    # R3
    "Montcada-Ripollet": [("Montcada Bifurcació", "R3"), ("La Florida", "R3")],
    "La Florida": [("Montcada-Ripollet", "R3"), ("Mollet-Santa Rosa", "R3")],
    "Mollet-Santa Rosa": [("Parets del Vallés", "R3"), ("La Florida", "R3")],
    "Parets del Vallés": [("Mollet-Santa Rosa", "R3"), ("Granollers-Canovelles", "R3")],
    "Granollers-Canovelles": [("Parets del Vallés", "R3"), ("Les Franqueses", "R3")],
    "Les Franqueses": [("La Garriga", "R3"), ("Granollers-Canovelles", "R3")],
    "La Garriga": [("Figaró", "R3"), ("Les Franqueses", "R3")],
    "Figaró": [("La Garriga", "R3"), ("Sant Martí de Centelles", "R3")],
    "Sant Martí de Centelles": [("Figaró", "R3"), ("Centelles", "R3")],
    "Centelles": [("Balenyà-Els Hostalets", "R3"), ("Sant Martí de Centelles", "R3")],
    "Balenyà-Els Hostalets": [("Balenyà-Tona-Seva", "R3"), ("Centelles", "R3")],
    "Balenyà-Tona-Seva": [("Balenyà-Els Hostalets", "R3"), ("Vic", "R3")],
    "Vic": [("Balenyà-Tona-Seva", "R3"), ("Manlleu", "R3")],
    "Manlleu": [("Torrelló", "R3"), ("Vic", "R3")],
    "Torrelló": [("Borgonyà", "R3"), ("Manlleu", "R3")],
    "Borgonyà": [("Torrelló", "R3"), ("Sant Quirze de Besora", "R3")],
    "Sant Quirze de Besora": [("Borgonyà", "R3")],

    # R1
    "Sant Adrià de Besòs": [("Clot", "R1"), ("Badalona", "R1")],
    "Badalona": [("Sant Adrià de Besòs", "R1"), ("Montgat", "R1")],
    "Montgat": [("Montgat Nord", "R1"), ("Badalona", "R1")],
    "Montgat Nord": [("El Masnou", "R1"), ("Montgat", "R1")],
    "El Masnou": [("Montgat Nord", "R1"), ("Ocata", "R1")],
    "Ocata": [("El Masnou", "R1"), ("Premià de Mar", "R1")],
    "Premià de Mar": [("Vilassar de Mar", "R1"), ("Ocata", "R1")],
    "Vilassar de Mar": [("Cabrera de Mar", "R1"), ("Premià de Mar", "R1")],
    "Cabrera de Mar": [("Vilassar de Mar", "R1"), ("Mataró", "R1")],
    "Mataró": [("Cabrera de Mar", "R1"), ("Sant Andreu de Llavaneres", "R1")],
    "Sant Andreu de Llavaneres": [("Caldes d'Estrac", "R1"), ("Mataró", "R1")],
    "Caldes d'Estrac": [("Arenys de Mar", "R1"), ("Sant Andreu de Llavaneres", "R1")],
    "Arenys de Mar": [("Caldes d'Estrac", "R1"), ("Canet de Mar", "R1")],
    "Canet de Mar": [("Arenys de Mar", "R1"), ("Sant Pol de Mar", "R1")],
    "Sant Pol de Mar": [("Calella", "R1"), ("Canet de Mar", "R1")],
    "Calella": [("Pineda de Mar", "R1"), ("Sant Pol de Mar", "R1")],
    "Pineda de Mar": [("Calella", "R1"), ("Santa Susanna", "R1")],
    "Santa Susanna": [("Pineda de Mar", "R1"), ("Malgrat de Mar", "R1")],
    "Malgrat de Mar": [("Blanes", "R1"), ("Santa Susanna", "R1")],
    "Blanes": [("Tordera", "R1"), ("Malgrat de Mar", "R1")],
    "Tordera": [("Blanes", "R1"), ("Maçanet-Massanes", "R1")],
}

COLORES_LINEA = {
    "R1": "#4FC3F7",
    "R2": "#66BB6A",
    "R2S": "#045C1B",
    "R2N": "#B5ED70",
    "R3": "#F91111",
    "R4": "#FFAF01",
    "R7": "#DD65E8",
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
                nuevo_coste += 5
                nuevos_cambios.append(nodo)
            heappush(cola, (nuevo_coste, vecino, linea, camino + [vecino], nuevos_cambios, lineas + [linea]))
    return None, None, None, None

def main(page: ft.Page):
    page.window.full_screen = True
    page.title = "Simulador Rodalies TR"
    page.bgcolor = "#1a1c1e"
    page.window_maximized = True

    state = {
        "grafo": copy.deepcopy(graf_base),
        "origen": None, "destino": None,
        "cerradas": set(), "camino": [], "cambios": [],
        "lineas_camino": []
    }

    cv_mapa = cv.Canvas(expand=True)
    info_text = ft.Text("Selecciona una estació d'origen", size=16, color=Colors.WHITE, weight="bold")

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

        # 3. Dibujar estaciones encima 
        for est, (x, y) in pos.items():
            dot_col = Colors.WHITE
            if est == state["origen"]:     dot_col = Colors.AMBER
            elif est == state["destino"]:  dot_col = Colors.RED
            elif est in state["camino"]:   dot_col = Colors.ORANGE
            elif est in state["cerradas"]: dot_col = Colors.GREY_700

            cv_mapa.shapes.append(cv.Circle(x, y, 9, paint=Paint(color=dot_col, style=PaintingStyle.FILL)))
            cv_mapa.shapes.append(cv.Circle(x, y, 9, paint=Paint(color="#555", stroke_width=2, style=PaintingStyle.STROKE)))

            tx, ty, angulo, align = calcular_etiqueta(est, x, y)
            cv_mapa.shapes.append(cv.Text(
                tx, ty, est,
                style=ft.TextStyle(size=10, color=Colors.WHITE),
                rotate=math.radians(angulo),
                text_align=align,
            ))

            if est in state["cerradas"]:
                cv_mapa.shapes.append(cv.Line(x-7, y-7, x+7, y+7, paint=Paint(color=Colors.RED, stroke_width=3)))
                cv_mapa.shapes.append(cv.Line(x-7, y+7, x+7, y-7, paint=Paint(color=Colors.RED, stroke_width=3)))
            if est in state["cambios"]:
                cv_mapa.shapes.append(cv.Text(x, y+18, "TRANSBORD",
                    ft.TextStyle(size=9, color=Colors.RED_ACCENT, weight="bold")))
        page.update()

    def on_click_izq(e: ft.TapEvent):
        for est, (x, y) in pos.items():
            if ((e.local_position.x - x)**2 + (e.local_position.y - y)**2)**0.5 < 22:
                if est in state["cerradas"]: return
                if state["origen"] is None:
                    state["origen"] = est
                    info_text.value = f"Origen: {est}. Tria destí."
                elif state["destino"] is None and est != state["origen"]:
                    state["destino"] = est
                    coste, camino, cambios, lineas = dijkstra(state["grafo"], state["origen"], state["destino"])
                    if camino:
                        state["camino"], state["cambios"], state["lineas_camino"] = camino, cambios, lineas
                        paradas = len(camino) - 1
                        if cambios:
                            detalle = ", ".join(cambios)
                            transbordos_txt = f" | {len(cambios)} transbordament{'s' if len(cambios) > 1 else ''} a {detalle}"
                        else:
                            transbordos_txt = " | Sense transbordament"
                        info_text.value = f"✅ {state['origen']} → {state['destino']} | {paradas} parades{transbordos_txt}"
                    else:
                        info_text.value = "❌ No hi ha cap ruta disponible"
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
                    info_text.value = f"⛔ {est} tancada"
                else:
                    state["cerradas"].discard(est)
                    state["grafo"] = copy.deepcopy(graf_base)
                    for cerrada in state["cerradas"]:
                        for v in state["grafo"]:
                            state["grafo"][v] = [(d, l) for d, l in state["grafo"][v] if d != cerrada]
                        state["grafo"][cerrada] = []
                    info_text.value = f"✅ {est} reoberta"
                dibujar_red()
                return

    def reset_all(e):
        state["grafo"] = copy.deepcopy(graf_base)
        state["cerradas"].clear()
        state["origen"] = state["destino"] = None
        state["camino"], state["cambios"], state["lineas_camino"] = [], [], []
        info_text.value = "Xarxa reiniciada"
        dibujar_red()

    mapa_interactivo = ft.GestureDetector(
        content=ft.Container(content=cv_mapa, expand=True),
        on_tap_down=on_click_izq,
        on_secondary_tap_down=on_click_der,
    )

    leyenda = ft.Row([
        ft.Text("━ R1", color="#4FC3F7", size=13, weight="bold"),
        ft.Text("━ R2", color="#66BB6A", size=13, weight="bold"),
        ft.Text("━ R2S", color="#045C1B", size=13, weight="bold"),
        ft.Text("━ R2N", color="#B5ED70", size=13, weight="bold"),
        ft.Text("━ R3", color="#F91111", size=13, weight="bold"),
        ft.Text("━ R4", color="#FFAF01", size=13, weight="bold"),
        ft.Text("━ R7", color="#DD65E8", size=13, weight="bold"),
        ft.Text("━ R8", color="#AE07DC", size=13, weight="bold"),

    ], spacing=15)

    controles = ft.Container(
        content=ft.Column([
            ft.Text("SIMULADOR DE RODALIES", size=26, weight="bold", color=Colors.AMBER),
            info_text,
            ft.Row([
                ft.ElevatedButton("Reiniciar", icon="refresh", on_click=reset_all),
                ft.Text("Click esq.: seleccionar | Click dret: tancar/reobrir",
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