from collections import deque

def bfs_transbordos(grafo, inicio, destino):
    cola = deque()
    cola.append((inicio, None, [inicio]))  
    visitados = set()

    while cola:
        nodo, linea_actual, camino = cola.popleft()

        if nodo == destino:
            return camino

        if (nodo, linea_actual) in visitados:
            continue

        visitados.add((nodo, linea_actual))

        for vecino, linea in grafo.get(nodo, []):
            nuevo_camino = list(camino)

            if linea_actual and linea != linea_actual:
                nuevo_camino.append(f"[TRANSBORDO a {linea}]")

            nuevo_camino.append(f"{vecino} ({linea})")

            cola.append((vecino, linea, nuevo_camino))

    return None

def jugar(grafo):
    print("=== BUSCADOR DE CAMINOS RODALIES ===")

    
    inicio = input("Estación origen: ")
    destino = input("Estación destino: ")

    if inicio not in grafo or destino not in grafo:
        print("Estación no válida\n")
        return()

    camino = bfs_transbordos(grafo, inicio, destino)

    if camino:
        print("✅ Camino encontrado:")
        print(" -> ".join(camino))
    else:
        print("❌ No hay conexión")

    print()

def eliminar_conexion(grafo, a, b):
    if a not in grafo or b not in grafo:
        print("Estación no válida\n")
        return

    grafo[a] = [(v,l) for v,l in grafo[a] if v != b]
    grafo[b] = [(v,l) for v,l in grafo[b] if v != a]

    print("Conexión eliminada\n") 

def eliminar_estacion(grafo, estacion):
    if estacion not in grafo:
        print("Estación no válida\n")
        return

    for vecino, _ in grafo[estacion]:
        grafo[vecino] = [(v, l) for v, l in grafo[vecino] if v != estacion]

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
# R2
"Castelldefels": [
    ("Gavà", "R2")
],
"Gavà":[
    ("Castelldefels", "R2"),
    ("Viladecans", "R2")
],
"Viladecans":[
    ("Gavà", "R2"),
    ("El Prat de Llobregat", "R2")
],
"El Prat de Llobregat":[
    ("Viladecans", "R2"),
    ("Bellvitge-Gornal", "R2")
],
"Bellvitge-Gornal":[
    ("El Prat de Llobregat", "R2"),
    ("Barcelona-Sants", "R2")
],
"Barcelona-Passeig de Gràcia":[
    ("Barcelona-Sants", "R2"),
    ("Barcelona-El Clot", "R2")
],
#Conexión
"Barcelona-Sants":[
    ("Bellvitge-Gornal", "R2"),
    ("L'Hospitalet de Llobregat", "R1"),
    ("Barcelona-Plaça de Catalunya", "R1"),
    ("Barcelona-Passeig de Gràcia", "R2")
],
"Barcelona-El Clot":[
    ("Barcelona-Arc de Triomf", "R1"),
    ("Barcelona-Passeig de Gràcia", "R2")
],

#R1
"Barcelona-Plaça de Catalunya":[
    ("Barcelona-Sants", "R1"),
    ("Barcelona-Arc de Triomf", "R1")
],
"L'Hospitalet de Llobregat":[
    ("Cornellà", "R1"),
    ("Barcelona-Sants", "R1")
],
"Cornellà":[
    ("L'Hospitalet de Llobregat", "R1"),
    ("Sant Joan Despí", "R1")
],
"Sant Joan Despí":[
    ("Cornellà", "R1"),
    ("Sant Feliu de Llobregat", "R1")
],
"Sant Feliu de Llobregat":[
    ("Sant Joan Despí", "R1"),
    ("Molins de Rei", "R1")
],
"Molins de Rei":[
    ("Sant Feliu de Llobregat", "R1")
],
}
menu(grafo)