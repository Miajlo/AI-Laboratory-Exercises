from random import randint
import queue

def find_disjoint_subgraph_count(graph):
    disjoint_count = 0

    processed_vertices = set()

    for vertex, edges in graph.items():
        if vertex in processed_vertices:
            continue

        q = queue.Queue()

        processed_vertices.add(vertex)

        q.put(vertex)

        while not q.empty():
            curr_vertex = q.get()
            for neighbor in graph[curr_vertex]:
                if neighbor not in processed_vertices:
                    processed_vertices.add(neighbor)
                    q.put(neighbor)

        disjoint_count += 1

    return disjoint_count



def generate_graph(vert_count, edge_count):
    graph = {}

    for i in range(vert_count):
        graph[i] = []

    edges_added = 0
    while edges_added < edge_count:
        # Pick two distinct vertices randomly
        vert = randint(0, vert_count - 1)
        edge = randint(0, vert_count - 1)

        if vert != edge and edge not in graph[vert]:
            graph[vert].append(edge)
            graph[edge].append(vert)
            edges_added += 1

    return graph


if __name__ == '__main__':


    graf = {
        1: [2, 3],
        2: [1],
        3: [1],
        5: [6],
        6: [5],
        7: [8],
        8: [7]
    }

    #graf = generate_graph(5000, 10)

    print(find_disjoint_subgraph_count(graf))