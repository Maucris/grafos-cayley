import os
import networkx as nx
import ultimo  


def exportar_grafo_etiquetado(n, tipo, prioridad=None, outdir="gexf"):
    if prioridad is None:
        prioridad = {}

    
    ultimo.n = n

    if tipo == "transposition":
        generadores = ultimo.generadores_transposition(n)
    elif tipo == "bubble":
        generadores = ultimo.generadores_bubble(n)
    elif tipo == "star":
        generadores = ultimo.generadores_star(n)
    elif tipo == "pancake":
        generadores = ultimo.generadores_pancake(n)
    else:
        raise ValueError("tipo inválido: transposition|bubble|star|pancake")

    # Construir grafo de Cayley
    G = ultimo.construir_grafo_cayley(generadores)

    
    nodo_inicio = tuple(range(1, n + 1))
    G = ultimo.bfs_etiquetado(G, nodo_inicio, prioridad=prioridad)

    #Exportar el grafo 
    os.makedirs(outdir, exist_ok=True)
    ruta = os.path.join(outdir, f"cayley_{tipo}_n{n}_bfs_etiquetado.gexf")
    nx.write_gexf(G, ruta)

    print(f"Exportado: {ruta}")
    print(f"  nodos={G.number_of_nodes()} aristas={G.number_of_edges()}")


if __name__ == "__main__":
    exportar_grafo_etiquetado(
        n=4,
        tipo="transposition",
        prioridad={'b': 0, 'c': 1}  
    )
