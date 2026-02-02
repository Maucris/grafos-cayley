
import networkx as nx # libreria para trabajar con grafos
import matplotlib.pyplot as plt # libreria para graficar
import string 
from collections import deque

# FUNCIONES PARA OBTENER LOS GENERADORES DE ARISTAS
def generadores_pancake(n):
    
    p1=tuple(range(1,n+1))
    aristas=[]
    for k in range(2, n + 1):
        volteo = p1[:k][::-1] + p1[k:]
        aristas.append(volteo)
        
    return aristas

def generadores_star(n):
    
    p1 = tuple(range(1, n+1))
    aristas = []
    
    for k in range(2, n + 1):
        
        perm = list(p1)
        
        
        perm[0], perm[k-1] = perm[k-1], perm[0]
        
        aristas.append(tuple(perm))
        
    return aristas

def generadores_bubble(n):
    
    p1 = tuple(range(1, n+1))
    aristas = []
    
    for i in range(n - 1):
        
        perm = list(p1)
        
        
        perm[i], perm[i+1] = perm[i+1], perm[i]
        
        aristas.append(tuple(perm))
        
    return aristas

def generadores_transposition(n):
    
    p1 = tuple(range(1, n+1))
    aristas = []
    
    
    for i in range(n):
        for j in range(i + 1, n):
            perm = list(p1)
            
            
            perm[i], perm[j] = perm[j], perm[i]
            
            aristas.append(tuple(perm))
    
    return aristas

def construir_grafo_cayley(generadores):
    G = nx.Graph()# creamos el grafo vacio 
    grado = len(generadores)

    letras = string.ascii_lowercase + string.ascii_uppercase + string.digits # genera una lista de letras minusculas, mayusculas y digitos

    letras_generadores = {generadores[i]: letras[i] for i in range(grado)}

    nodo_base = tuple(range(1, n+1)) #  nodo base es la permutacion identidad
    nodos = [nodo_base] #se crea una lista de nodos que inicia con el nodo base
    visitados = set(nodos) #visitados es un conjunto que contiene los nodos ya visitados para evitar duplicados

    i = 0 #indice para recorrer la lista de nodos
    while i < len(nodos): #mientras el indice sea menor que la longitud de la lista de nodos
        nodo_actual = nodos[i] #nodo actual es el nodo que se encuentre en el indice i
        i += 1 #incrementamos el indice para la siguiente iteracion

        for generador in generadores: # recoremos los generadores de aristas
            nuevo_nodo = tuple(
                nodo_actual[generador[j] - 1]
                for j in range(n)# creamos un nuevo nodo recoriendo el generador de arista 
            )

            if nuevo_nodo not in visitados: #si ese nodo aun no lo hemos visitado
                visitados.add(nuevo_nodo) # agregamos al conjunto de nodos visitados el nuevo nodo 
                nodos.append(nuevo_nodo) # agregamos el nodo a la lista de nodos 


            G.add_edge(nodo_actual, nuevo_nodo, label=letras_generadores[generador]) # agregamos la etiqueta a la arista

    return G


def dibujar_grafo(G):
    pos = nx.spring_layout(G, seed=30, k=4)

    plt.figure(figsize=(12, 10))

    # Etiquetas de nodos
    etiquetas_nodos = {nodo: str(nodo) for nodo in G.nodes()}

    # Dibujar el grafo
    nx.draw(
        G,
        pos,
        labels=etiquetas_nodos,
        node_size=600,
        node_color="#9bd2f9",
        font_size=8,
        edge_color="#cccccc"
    )

    # Obtener etiquetas de aristas
    etiquetas_aristas = nx.get_edge_attributes(G, 'label')

    # Dibujar etiquetas de aristas
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=etiquetas_aristas,
        font_size=6
    )

    plt.axis("off")
    plt.show()

###

def bfs_etiquetado(G, nodo_inicio, prioridad=None):
    G.nodes[nodo_inicio]["label"] = "$" # asignamos la etiqueta inicial al nodo de inicio
    cola = deque([nodo_inicio])# inicializamos la cola con el nodo de inicio
    visitados = {nodo_inicio} #se crea un conjunto de nodos visitados que inicia con el nodo de inicio

    if prioridad is None:
        prioridad = {}

    indice = 0

    while cola: 
        nodo_actual = cola.popleft() # sacamos el primer nodo de la cola

        # Obtener vecinos junto con la etiqueta de la arista
        vecinos = []
        for vecino in G.neighbors(nodo_actual): # recorremos los vecinos del nodo actual
            label = G[nodo_actual][vecino].get("label") # obtenemos la etiqueta de la arista entre el nodo actual y el vecino
            vecinos.append((label, vecino)) # agregamos una tupla (etiqueta, vecino) a la lista de vecinos

        # ORDENAR
        vecinos.sort(key=lambda x: (prioridad.get(x[0], 9999), x[0])) # ordenar los vecinos por la etiqueta de la arista

        #BFS en ese orden
        for label, vecino in vecinos: # recorremos los vecinos ordenados
            if vecino not in visitados: # si el vecino no ha sido visitado
                visitados.add(vecino) # lo marcamos como visitado
                cola.append(vecino) # lo agregamos a la cola

                indice += 1
                G.nodes[vecino]["label"] = str((G.nodes[nodo_actual]["label"] + label).replace("$","")) # asignamos la etiqueta al nodo vecino

    return G # devolvemos el grafo con las etiquetas asignadas a los nodos


def dibujar_grafo_bfs(G):
   
    pos = nx.spring_layout(G, seed=42, k=1.2)# posicionamiento de los nodos

    plt.figure(figsize=(12, 10))                                                        

    nx.draw(
        G,
        pos,
        labels= nx.get_node_attributes(G,"label"), #etiquetas_nodos,   
        node_size=600,
        node_color="#9bd2f9",
        font_size=12,
        edge_color="#cccccc"
    )

    etiquetas_aristas = nx.get_edge_attributes(G, 'label')

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=etiquetas_aristas,
        font_size=6
    )

    plt.axis("off")
    plt.show()


#n=4 # numero de elementos en la permutacion
#generadores = generadores_transposition(n) #invocamos la funcion generadores  para obtener las aristas posibles
#G = construir_grafo_cayley(generadores) # CREAMOS EL GRAFO DESEADO
#dibujar_grafo(G) # DIBUJAMOS EL GRAFO

#nodo_inicio = (1,2,3,4)    # nodo de inicio para el BFS

#prioridad ={'b': 0, 'c':1}

#G = bfs_etiquetado(G, nodo_inicio, prioridad=prioridad) # REALIZAMOS EL BFS ETIQUETANDO LOS NODOS

#dibujar_grafo_bfs(G) # DIBUJAMOS EL GRAFO ETIQUETADO
