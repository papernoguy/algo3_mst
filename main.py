from queue import PriorityQueue
from random import randint

from pip._internal.vcs import git


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        s = "VERTEX [" + str(self.id) + "] \n"
        for x in self.adjacent:
            s = s + ('adjacent [' + str(x.id) + ']  weight= ' + str(self.get_weight(x)) + '\n')
        return s

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def remove_neighbor(self, neighbor, weight=0):
        self.adjacent.pop(neighbor)

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
        self.num_edges = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def __str__(self):
        s = 'Graph total: vertices: %s edges: %s \n' % (self.num_vertices, self.num_edges)
        for v in self:
            s = s + str(self.vert_dict[v.get_id()]) + "\n"
        return s

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def get_vertices(self):
        return self.vert_dict.keys()

    def add_vertex(self, node):
        if node not in self.vert_dict:
            self.num_vertices = self.num_vertices + 1
            new_vertex = Vertex(node)
            self.vert_dict[node] = new_vertex
            return new_vertex
        return None

    def add_edge(self, frm, to, weight=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        if not self.vert_dict[frm] in self.vert_dict[to].adjacent:  # if edge already exists do not update counter
            self.num_edges = self.num_edges + 1
            self.vert_dict[to].add_neighbor(self.vert_dict[frm], weight)
            self.vert_dict[frm].add_neighbor(self.vert_dict[to], weight)

    def add_edges_from(self, edges):
        for i in range(len(edges)):
            frm = (edges[i])[0]
            to = (edges[i])[1]
            weight = (edges[i])[2]
            self.add_edge(frm, to, weight)

    def __dfs_find_path(self, start, end, path=[]):  # helper function for mst_add_edge
        start = self.get_vertex(start)
        end = self.get_vertex(end)
        neighbors = start.get_connections()
        path = path + [start]
        if start == end:
            return path
        for node in list(neighbors):
            if node not in path:
                newpath = self.__dfs_find_path(node.id, end.id, path)
                if newpath:
                    return newpath

    def mst_add_edge(self, edge):
        circle = self.__dfs_find_path(edge[0], edge[1])
        w_pqueue = PriorityQueue()  # maximum priority queue using negative weight
        w_pqueue.put((-edge[2], edge))
        for i in range(len(circle) - 1):
            weight = circle[i].get_weight(circle[i + 1])
            w_pqueue.put((-weight, (circle[i].id, circle[i + 1].id)))
        _, heaviest_edge = w_pqueue.get()
        if heaviest_edge != edge:
            self.add_edge(edge[0], edge[1], edge[2])
            self.remove_edge(*heaviest_edge)
            print("mst_add_edge::: given edge changed the mst ")
        else:
            print("mst_add_edge::: given edge did not change the mst ")

    def remove_edge(self, frm, to, weight=0):
        self.vert_dict[to].remove_neighbor(self.vert_dict[frm], weight)
        self.vert_dict[frm].remove_neighbor(self.vert_dict[to], weight)
        self.num_edges = self.num_edges - 1

    def mst_prim(self, root):
        mst_g = Graph()
        visited = set()
        pqueue = PriorityQueue()
        start = self.get_vertex(root)
        for neighbor in list(start.get_connections()):
            edge_weight = start.get_weight(neighbor)
            pqueue.put((edge_weight, (start.id, neighbor.id)))

        while len(visited) < self.num_vertices:
            _, edge = pqueue.get(pqueue)
            if edge[0] not in visited:
                new_node = edge[0]
            elif edge[1] not in visited:
                new_node = edge[1]
            else:
                continue

            start = self.get_vertex(new_node)
            for neighbor in list(start.get_connections()):
                edge_weight = start.get_weight(neighbor)
                pqueue.put((edge_weight, (start.id, neighbor.id)))

            mst_g.add_edge(edge[0], edge[1], self.get_vertex(edge[0]).get_weight(self.get_vertex(edge[1])))
            visited.add(new_node)

        self.vert_dict = mst_g.vert_dict
        self.num_edges = mst_g.num_edges
        self.num_vertices = mst_g.num_vertices

    def random_graph_generator(self, nodes, edges, weight_range):
        for i in range(1, nodes):
            self.add_vertex(i)
        while self.num_edges <= edges:
            self.add_edge(randint(1, nodes), randint(1, nodes), randint(0, weight_range))


if __name__ == '__main__':
    print("Guy Paperno 208508143 גיא פפרנו \n Amit Ophir 322526880 עמית אופיר")
    g = Graph()
    g.add_edges_from(
        [(10, 11, 18), (12, 9, 26), (16, 6, 83), (2, 5, 91), (3, 19, 47), (5, 14, 88), (16, 2, 53), (19, 15, 85),
         (10, 7, 1), (19, 5, 97), (8, 8, 98), (19, 6, 52), (3, 13, 18), (13, 13, 63), (2, 3, 36), (20, 10, 38),
         (14, 19, 1), (4, 13, 46), (11, 5, 19), (11, 11, 40), (16, 1, 99), (15, 6, 28), (13, 2, 80), (10, 7, 57),
         (1, 9, 41), (13, 11, 86), (7, 15, 75), (14, 10, 12), (7, 16, 28), (19, 20, 13), (19, 17, 98), (12, 11, 83),
         (15, 1, 87), (8, 10, 72), (16, 18, 71), (4, 14, 60), (16, 3, 55), (15, 7, 94), (17, 15, 69), (1, 20, 22),
         (4, 18, 19), (10, 15, 99), (4, 5, 2), (10, 11, 60), (2, 11, 16), (18, 4, 18), (9, 8, 86), (15, 3, 60),
         (20, 2, 84), (6, 7, 74), (12, 14, 55), (12, 16, 6), (7, 8, 70), (1, 5, 62)])
    print(g)

    g.mst_prim(5)
    print(g)

    new_edge = (1, 2, 100)
    print("edge (", new_edge[0], ",", new_edge[1], "weight=", new_edge[2], ")")
    g.mst_add_edge(new_edge)
    print(g)

    new_edge = (2, 20, 1)
    print("edge (", new_edge[0], ",", new_edge[1], "weight=", new_edge[2], ")")
    g.mst_add_edge(new_edge)
    print(g)

    g1 = Graph()
    g1.random_graph_generator(20, 50, 99)
