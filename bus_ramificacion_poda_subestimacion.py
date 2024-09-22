import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

G = nx.Graph()

nodos = ['A', 'C', 'D', 'E', 'F', 'B']
G.add_nodes_from(nodos)

aristas_con_pesos = [
    ('A', 'D', 2),
    ('A', 'C', 3),
    ('C', 'E', 2),
    ('E', 'F', 3),
    ('D', 'F', 3),
    ('C', 'D', 4),
    ('E', 'B', 4),
    ('F', 'B', 5)
]

G.add_weighted_edges_from(aristas_con_pesos)

posiciones = {
    'A': (-2, 1),
    'C': (0, 2),
    'D': (0, -1),
    'E': (4, 2),
    'F': (4, -1),
    'B': (8, 1),
}

arbol = {
    'A': ['C', 'D'],
    'C': ['A', 'D', 'E'],
    'D': ['A', 'C', 'F'],
    'E': ['C', 'F', 'B'],
    'F': ['D', 'E', 'B'],
    'B': ['E', 'F']
}

# Dibujar los nodos
plt.figure(figsize=(8, 6))
nx.draw(G, posiciones, with_labels=True, node_color='red', edge_color='black', node_size=2000, font_size=16, font_weight='bold')

# Dibujar los pesos de las aristas
etiquetas = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas, font_size=12)

# Mostrar grafo
plt.grid(True)
plt.show()

def construir_arbol_binario(grafo, nodo_actual, visitados):
    # Crea un nodo para el árbol binario
    raiz = Nodo(nodo_actual)
    visitados.add(nodo_actual)

    # Obtiene los vecinos del nodo actual
    vecinos = [vecino for vecino in grafo[nodo_actual] if vecino not in visitados]

    if vecinos:
        # El primer vecino lo asignamos como hijo izquierdo
        raiz.izquierda = construir_arbol_binario(grafo, vecinos[0], visitados.copy())

        # Si hay más de un vecino, el segundo lo asignamos como hijo derecho
        if len(vecinos) > 1:
            raiz.derecha = construir_arbol_binario(grafo, vecinos[1], visitados.copy())

    return raiz

# Función para imprimir el árbol binario
def imprimir_arbol(raiz, nivel=0, lado="Raíz"):
    if raiz is not None:
        print("  " * nivel + f"{lado}: {raiz.valor}")
        imprimir_arbol(raiz.izquierda, nivel + 1, "Izq")
        imprimir_arbol(raiz.derecha, nivel + 1, "Der")

# Función de heurística basada en la distancia euclidiana entre nodos
def heuristica_euclidiana(posiciones, nodo_actual, nodo_objetivo):
    x1, y1 = posiciones[nodo_actual]
    x2, y2 = posiciones[nodo_objetivo]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def busqueda_y_poda_camino_mas_corto_con_heuristica(grafo, posiciones, inicio, fin):
    # Cola de prioridad para explorar nodos (costo total estimado, costo acumulado, camino, nodo actual)
    cola_prioridad = [(heuristica_euclidiana(posiciones, inicio, fin), 0, [inicio])]
    # Diccionario para almacenar el costo conocido más bajo para cada nodo
    mejor_costo = {inicio: 0}

    while cola_prioridad:
        estimacion_total, costo_actual, camino = heapq.heappop(cola_prioridad)
        nodo_actual = camino[-1]

        # Mostrar el estado actual de la cola de prioridad y el camino actual
        print(f"Explorando nodo: {nodo_actual}")
        print(f"Camino actual: {camino}")
        print(f"Costo acumulado: {costo_actual}")
        print(f"Estimación total (costo acumulado + heurística): {estimacion_total}")
        print(f"Cola de prioridad: {cola_prioridad}")
        print('-' * 40)

        # Si se llega al destino, retornar el camino y el costo
        if nodo_actual == fin:
            return costo_actual, camino

        for vecino in grafo.neighbors(nodo_actual):
            peso_arista = grafo.get_edge_data(nodo_actual, vecino)['weight']
            nuevo_costo = costo_actual + peso_arista
            nuevo_camino = camino + [vecino]

            # Estimación del costo total incluyendo la heurística
            estimacion_total = nuevo_costo + heuristica_euclidiana(posiciones, vecino, fin)

            if vecino not in mejor_costo or nuevo_costo < mejor_costo[vecino]:
                mejor_costo[vecino] = nuevo_costo
                heapq.heappush(cola_prioridad, (estimacion_total, nuevo_costo, nuevo_camino))

    return float('inf'), []

# Ejemplo de uso con el grafo dado
nodo_inicio = 'A'
nodo_fin = 'B'
arbol_binario = construir_arbol_binario(arbol, 'A', set())
imprimir_arbol(arbol_binario)
costo, camino = busqueda_y_poda_camino_mas_corto_con_heuristica(G, posiciones, nodo_inicio, nodo_fin)
print(f"Camino final: {camino}")
print(f"Costo final: {costo}")