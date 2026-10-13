from collections import deque

def bfs_camino(grafo, inicio, destino):
    cola = deque([[inicio]])
    visitados = set()

    while cola:
        camino = cola.popleft()
        nodo = camino[-1]

        if nodo == destino:
            return camino

        if nodo not in visitados:
            visitados.add(nodo)

            for vecino in grafo.get(nodo, []):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)

    return None

def jugar(grafo):
    print("=== BUSCADOR DE CAMINOS RODALIES ===")

    
    inicio = input("Estación origen: ")
    destino = input("Estación destino: ")

    if inicio not in grafo or destino not in grafo:
        print("Estación no válida\n")
        return()

    camino = bfs_camino(grafo, inicio, destino)

    if camino:
        print("✅ Camino encontrado:")
        print(" -> ".join(camino))
    else:
        print("❌ No hay conexión")

    print()

def eliminar_conexion(grafo, a, b):
    if a not in grafo or b not in grafo:
        print("Estación no válida\n")
        return()
    if b in grafo[a] and a in grafo[b]:
        grafo[a].remove(b)
        grafo[b].remove(a)
        print("Conexión eliminada\n")
    else:
        print("Esta conexión no existe")
        

def eliminar_estacion(grafo, estacion):
    for vecino in grafo[estacion]:
        grafo[vecino].remove(estacion)
    del grafo[estacion]

def menu(grafo):
    while True:
        print("1. Buscar camino")
        print("2. Cortar conexión")
        print("3. Cerrar estación")
        print("4. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            jugar(grafo)

        elif opcion == "2":
            a = input("Estación A: ")
            b = input("Estación B: ")
            eliminar_conexion(grafo, a, b)

        elif opcion == "3":
            est = input("Estación: ")
            eliminar_estacion(grafo, est)
            print("Estación eliminada\n")

        elif opcion == "4":
            break

grafo = {
# ===== R1 =====
"Maçanet-Massanes": ["Blanes"],
"Blanes": ["Maçanet-Massanes", "Tordera"],
"Tordera": ["Blanes", "Malgrat de Mar"],
"Malgrat de Mar": ["Tordera", "Santa Susanna"],
"Santa Susanna": ["Malgrat de Mar", "Pineda de Mar"],
"Pineda de Mar": ["Santa Susanna", "Calella"],
"Calella": ["Pineda de Mar", "Sant Pol de Mar"],
"Sant Pol de Mar": ["Calella", "Canet de Mar"],
"Canet de Mar": ["Sant Pol de Mar", "Arenys de Mar"],
"Arenys de Mar": ["Canet de Mar", "Caldes d'Estrac"],
"Caldes d'Estrac": ["Arenys de Mar", "Sant Andreu de Llavaneres"],
"Sant Andreu de Llavaneres": ["Caldes d'Estrac", "Mataró"],
"Mataró": ["Sant Andreu de Llavaneres", "Cabrera de Mar-Vilassar de Mar"],
"Cabrera de Mar-Vilassar de Mar": ["Mataró", "Premià de Mar"],
"Premià de Mar": ["Cabrera de Mar-Vilassar de Mar", "Ocata"],
"Ocata": ["Premià de Mar", "El Masnou"],
"El Masnou": ["Ocata", "Montgat Nord"],
"Montgat Nord": ["El Masnou", "Montgat"],
"Montgat": ["Montgat Nord", "Badalona"],
"Badalona": ["Montgat", "Sant Adrià de Besòs"],
"Sant Adrià de Besòs": ["Badalona", "Barcelona-El Clot-Aragó"],

# ===== NÚCLEO BARCELONA =====
"Barcelona-El Clot-Aragó": ["Sant Adrià de Besòs", "Arc de Triomf", "Sant Andreu Arenal", "Passeig de Gràcia"],
"Arc de Triomf": ["Barcelona-El Clot-Aragó", "Plaça Catalunya"],
"Plaça Catalunya": ["Arc de Triomf", "Barcelona-Sants", "Passeig de Gràcia"],
"Passeig de Gràcia": ["Plaça Catalunya", "Barcelona-Sants", "Barcelona-El Clot-Aragó"],
"Barcelona-Sants": ["Plaça Catalunya", "L'Hospitalet de Llobregat", "Passeig de Gràcia"],
"L'Hospitalet de Llobregat": ["Barcelona-Sants", "Bellvitge"],
"Bellvitge": ["L'Hospitalet de Llobregat", "El Prat de Llobregat"],

# ===== R2 =====
"El Prat de Llobregat": ["Bellvitge", "Viladecans", "Aeroport"],
"Aeroport": ["El Prat de Llobregat"],
"Viladecans": ["El Prat de Llobregat", "Gavà"],
"Gavà": ["Viladecans", "Castelldefels"],
"Castelldefels": ["Gavà", "Platja de Castelldefels"],
"Platja de Castelldefels": ["Castelldefels", "Garraf"],
"Garraf": ["Platja de Castelldefels", "Sitges"],
"Sitges": ["Garraf", "Vilanova i la Geltrú"],
"Vilanova i la Geltrú": ["Sitges", "Cubelles"],
"Cubelles": ["Vilanova i la Geltrú", "Cunit"],
"Cunit": ["Cubelles", "Segur de Calafell"],
"Segur de Calafell": ["Cunit", "Calafell"],
"Calafell": ["Segur de Calafell", "Sant Vicenç de Calders"],

# ===== R2 NORD =====
"Sant Andreu Arenal": ["Barcelona-El Clot-Aragó", "Torre Baró"],
"Torre Baró": ["Sant Andreu Arenal", "Montcada i Reixac"],
"Montcada i Reixac": ["Torre Baró", "Mollet Sant Fost"],
"Mollet Sant Fost": ["Montcada i Reixac", "Granollers Centre"],
"Granollers Centre": ["Mollet Sant Fost", "Cardedeu"],
"Cardedeu": ["Granollers Centre", "Llinars del Vallès"],
"Llinars del Vallès": ["Cardedeu", "Sant Celoni"],
"Sant Celoni": ["Llinars del Vallès", "Hostalric"],
"Hostalric": ["Sant Celoni", "Maçanet-Massanes"],

# ===== R3 =====
"Hospitalet de Llobregat": ["Barcelona-Sants", "Barcelona-Plaça Catalunya"],
"Vic": ["Manlleu", "Balenyà-Tona-Seva"],
"Manlleu": ["Torelló", "Vic"],
"Torelló": ["Manlleu"],
"Balenyà-Tona-Seva": ["Vic", "Centelles"],
"Centelles": ["Balenyà-Tona-Seva", "Figaró"],
"Figaró": ["Centelles", "La Garriga"],
"La Garriga": ["Figaró", "Les Franqueses"],
"Les Franqueses": ["La Garriga", "Granollers-Canovelles"],
"Granollers-Canovelles": ["Les Franqueses", "Montcada Bifurcació"],
"Montcada Bifurcació": ["Granollers-Canovelles", "Barcelona-Sant Andreu Arenal"],

# ===== R4 =====
"Manresa": ["Sant Vicenç de Castellet"],
"Sant Vicenç de Castellet": ["Manresa", "Terrassa"],
"Terrassa": ["Sant Vicenç de Castellet", "Sabadell"],
"Sabadell": ["Terrassa", "Cerdanyola del Vallès"],
"Cerdanyola del Vallès": ["Sabadell", "Barcelona-Sants"],
"Martorell": ["Sant Sadurní d'Anoia"],
"Sant Sadurní d'Anoia": ["Martorell", "Vilafranca del Penedès"],
"Vilafranca del Penedès": ["Sant Sadurní d'Anoia", "Sant Vicenç de Calders"],
"Sant Vicenç de Calders": ["Vilafranca del Penedès", "Calafell"],

# ===== R7 / R8 =====
"Cerdanyola Universitat": ["Cerdanyola del Vallès"],
"Rubí": ["Sant Cugat del Vallès"],
"Sant Cugat del Vallès": ["Rubí", "Cerdanyola Universitat"],

# ===== REGIONALES =====
"Tarragona": ["Reus", "Torredembarra"],
"Reus": ["Tarragona"],
"Torredembarra": ["Tarragona", "Sant Vicenç de Calders"],
"Lleida": ["Mollerussa"],
"Mollerussa": ["Lleida", "Tàrrega"],
"Tàrrega": ["Mollerussa", "Cervera"],
"Cervera": ["Tàrrega"],
"Girona": ["Flaçà"],
"Flaçà": ["Girona", "Figueres"],
"Figueres": ["Flaçà"]
}
menu(grafo)