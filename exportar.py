import os
import networkx as nx
import cayley_graphs  


def exportar_grafo_etiquetado(n, tipo, prioridad=None, outdir="gexf"):
    if prioridad is None:
        prioridad = {}

    
    cayley_graphs.n = n

    if tipo == "transposition":
        generadores = cayley_graphs.generadores_transposition(n)
    elif tipo == "bubble":
        generadores = cayley_graphs.generadores_bubble(n)
    elif tipo == "star":
        generadores = cayley_graphs.generadores_star(n)
    elif tipo == "pancake":
        generadores = cayley_graphs.generadores_pancake(n)
    else:
        raise ValueError("tipo inválido: transposition|bubble|star|pancake")

    # Construir grafo de Cayley
    G = cayley_graphs.construir_grafo_cayley(generadores)

    
    nodo_inicio = tuple(range(1, n + 1))
    G = cayley_graphs.bfs_etiquetado(G, nodo_inicio, prioridad=prioridad)

    #Exportar el grafo 
    os.makedirs(outdir, exist_ok=True)
    ruta = os.path.join(outdir, f"cayley_{tipo}_n{n}_bfs_etiquetado.gexf")
    nx.write_gexf(G, ruta)

    print(f"Exportado: {ruta}")
    print(f"  nodos={G.number_of_nodes()} aristas={G.number_of_edges()}")


if __name__ == "__main__":
    exportar_grafo_etiquetado(
        n=8,
        tipo="transposition",
        prioridad={'b': 0, 'c': 1}  
    )
