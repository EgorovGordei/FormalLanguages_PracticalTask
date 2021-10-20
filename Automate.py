
class AutomateNoWayException(Exception):
    "Automate's exception. Indicates that there is no edge from current node with specific letter"
    pass


class Edge:
    "Supporting class for Automate. Contains information about edge"
    def __init__(self, index, index_from, index_to, letter):
        self.index_from = index_from
        self.index_to = index_to
        self.letter = letter
        self.index = index

    def __repr__(self):
        return "["+"index:"+str(self.index)+" from:"+str(self.index_from)+" to:"+str(self.index_to)+" letter:"+self.letter+"]"


class Node:
    "Supporting class for Automate. Contains information about node"
    def __init__(self, index, finish):
        self.edges = []
        self.index = index
        self.finish = finish

    def add_edge(self, edge_index):
        self.edges.append(edge_index)

    def __repr__(self):
        return "["+"index:"+str(self.index)+" finish:"+str(self.finish)+" edges:"+str(self.edges)+"]"


class Automate:
    def __init__(self, reg_ex):
        self.current_node = 0
        self.edges = []
        self.nodes = []
        self.start_node = 0
        queue = []
        current_node_index = 0
        current_edge_index = 0
        finish_node = -1
        for c in reg_ex:
            if c in ["a","b","c"]:
                # create new sub-automate
                self.start_node = current_node_index
                queue.append([current_node_index, current_node_index+1])
                self.nodes.append(Node(current_node_index, False))
                self.nodes.append(Node(current_node_index+1, False))
                self.nodes[-2].add_edge(current_edge_index)
                self.edges.append(Edge(current_edge_index, current_node_index, current_node_index+1, c))
                current_edge_index += 1
                current_node_index += 2
            if c == "1":
                # create automate with 1 node
                self.start_node = current_node_index
                queue.append([current_node_index, current_node_index])
                self.nodes.append(Node(current_node_index, False))
                current_node_index += 1
            if c == ".":
                if len(queue) < 2:
                    raise ValueError()
                # connect last two automates consequently
                last_1 = queue[-1]
                queue.pop()
                last_0 = queue[-1]
                queue.pop()
                queue.append([last_0[0], last_1[1]])
                self.nodes[last_0[1]].add_edge(current_edge_index)
                self.edges.append(Edge(current_edge_index, last_0[1], last_1[0], ""))
                current_edge_index += 1
                self.start_node = last_0[0]
                finish_node = last_1[1]
            if c == "+":
                if len(queue) < 2:
                    raise ValueError()
                # connect last two automates in parallel
                last_1 = queue[-1]
                queue.pop()
                last_0 = queue[-1]
                queue.pop()
                queue.append([current_node_index, current_node_index+1])
                self.nodes.append(Node(current_node_index, False))
                self.nodes.append(Node(current_node_index+1, False))
                self.edges.append(Edge(current_edge_index, current_node_index, last_0[0], ""))
                self.edges.append(Edge(current_edge_index+1, current_node_index, last_1[0], ""))
                self.edges.append(Edge(current_edge_index+2, last_0[1], current_node_index+1, ""))
                self.edges.append(Edge(current_edge_index+3, last_1[1], current_node_index+1, ""))
                self.nodes[current_node_index].add_edge(current_edge_index)
                self.nodes[current_node_index].add_edge(current_edge_index+1)
                self.nodes[last_0[1]].add_edge(current_edge_index+2)
                self.nodes[last_1[1]].add_edge(current_edge_index+3)
                self.start_node = current_node_index
                finish_node = current_node_index + 1
                current_node_index += 2
                current_edge_index += 4
            if c == "*":
                if len(queue) < 1:
                    raise ValueError()
                # creates cycle from last automate
                last_0 = queue[-1]
                queue.pop()
                queue.append([current_node_index, current_node_index])
                self.nodes.append(Node(current_node_index, False))
                self.nodes[current_node_index].add_edge(current_edge_index)
                self.nodes[last_0[1]].add_edge(current_edge_index+1)
                self.edges.append(Edge(current_edge_index, current_node_index, last_0[0], ""))
                self.edges.append(Edge(current_edge_index+1, last_0[1], current_node_index, ""))
                self.start_node = current_node_index
                finish_node = current_node_index
                current_edge_index += 2
                current_node_index += 1
        if len(queue) != 1:
            raise ValueError()
        self.nodes[finish_node].finish = True

    def reverse(self):
        # find finish node
        finish_node = -1
        for node in self.nodes:
            if node.finish:
                if finish_node == -1:
                    finish_node = node.index
                else:
                    raise NotImplementedError()
        if finish_node == -1:
            raise NotImplementedError()
        # switch finish and start
        self.nodes[finish_node].finish = False
        self.nodes[self.start_node].finish = True
        self.start_node = finish_node
        # reverse all edges
        for e in self.edges:
            e.index_from, e.index_to = e.index_to, e.index_from
        for node in self.nodes:
            node.new_edges = []
        for e in self.edges:
            self.nodes[e.index_from].new_edges.append(e.index)
        for node in self.nodes:
            node.edges = node.new_edges
            node.new_edges = None

    def determinise(self):
        # remove empty edges
        for node in self.nodes:
            # find all nodes which are reachable via empty word
            epsylon_nodes = []
            for e in node.edges:
                if self.edges[e].letter == "":
                    epsylon_nodes.append(self.edges[e].index_to)
            if epsylon_nodes == []:
                continue
            new_nodes = [n for n in epsylon_nodes]
            while len(new_nodes) > 0:
                last_node = new_nodes.pop()
                for e in self.nodes[last_node].edges:
                    if self.edges[e].letter == "" and not self.edges[e].index_to in epsylon_nodes:
                        epsylon_nodes.append(self.edges[e].index_to)
                        new_nodes.append(self.edges[e].index_to)
            # create new edges
            for n in epsylon_nodes:
                if self.nodes[n].finish:
                    node.finish = True
                len_edges = len(self.nodes[n].edges)
                for i in range(len_edges):
                    e = self.nodes[n].edges[i]
                    if self.edges[e].letter != "":
                        self.edges.append(Edge(len(self.edges), node.index, self.edges[e].index_to, self.edges[e].letter))
                        node.add_edge(len(self.edges)-1)
        for node in self.nodes:
            i = 0
            while i < len(node.edges):
                if self.edges[node.edges[i]].letter == "":
                    node.edges = node.edges[0:i] + node.edges[i+1:]
                    i -= 1
                i += 1
        # find finish nodes
        finish_nodes = []
        for node in self.nodes:
            if node.finish:
                finish_nodes.append(node.index)
        if finish_nodes == []:
            raise NotImplementedError()
        # determinise
        used = set()
        edges = list()
        queue = [tuple([self.start_node])]
        # find new nodes
        while len(queue) > 0:
            n = queue.pop()
            if n in used:
                continue
            used.add(n)
            for c in "abc":
                new_node = set()
                for old_node in n:
                    for e in self.nodes[old_node].edges:
                        if self.edges[e].letter == c:
                            new_node.add(self.edges[e].index_to)
                new_node = list(new_node)
                new_node.sort()
                edges.append([n,tuple(new_node),c])
                queue.append(tuple(new_node))
        # construct new automate
        self.nodes = []
        self.edges = []
        nodes_indexes = dict()
        for n in used:
            nodes_indexes[n] = len(self.nodes)
            is_finish = False
            for fn in finish_nodes:
                if fn in n:
                    is_finish = True
                    break
            self.nodes.append(Node(len(self.nodes), is_finish))
        self.start_node = nodes_indexes[tuple([self.start_node])]
        for e in edges:
            self.edges.append(Edge(len(self.edges), nodes_indexes[e[0]], nodes_indexes[e[1]], e[2]))
            self.nodes[nodes_indexes[e[0]]].add_edge(len(self.edges) - 1)
        # remove nodes which can not reach finish
        bad_nodes = set()
        good_nodes = set()
        for i in range(len(self.nodes)):
            used_nodes, is_finish_reached = self.bfs(i)
            if is_finish_reached:
                good_nodes = good_nodes.union(used_nodes)
            else:
                bad_nodes = bad_nodes.union(used_nodes)
        self.start_node -= sum([(1 if j < self.start_node else 0) for j in bad_nodes])
        replaces_nodes = [-1 if self.nodes[i].index in bad_nodes else (i-sum([(1 if j < self.nodes[i].index else 0) for j in bad_nodes])) for i in range(len(self.nodes))]
        for n in self.nodes:
            n.index = replaces_nodes[n.index]
        bad_edges = set()
        for e in self.edges:
            e.index_from = replaces_nodes[e.index_from]
            e.index_to = replaces_nodes[e.index_to]
            if e.index_from == -1 or e.index_to == -1:
                bad_edges.add(e.index)
                e.index = -1
        replaces_edges = [-1 if self.edges[i].index == -1 else (i-sum([(1 if j < self.edges[i].index else 0) for j in bad_edges])) for i in range(len(self.edges))]
        for n in self.nodes:
            for i in range(len(n.edges)):
                n.edges[i] = replaces_edges[n.edges[i]]
        for e in self.edges:
            if e.index != -1:
                e.index = replaces_edges[e.index]
        i = 0
        while i < len(self.nodes):
            if self.nodes[i].index == -1:
                self.nodes = self.nodes[0:i] + self.nodes[i+1:]
                i -= 1
            else:
                j = 0
                while j < len(self.nodes[i].edges):
                    if self.nodes[i].edges[j] == -1:
                        self.nodes[i].edges = self.nodes[i].edges[0:j] + self.nodes[i].edges[j+1:]
                        j -= 1
                    j += 1
            i += 1
        i = 0
        while i < len(self.edges):
            if self.edges[i].index == -1:
                self.edges = self.edges[0:i] + self.edges[i+1:]
                i -= 1
            i += 1

    def bfs(self, node):
        "returns shortest word reachable from 'node' or all visited nodes if there is no word"
        used = set([node])
        came_from = dict()
        queue = [node]
        came_from[node] = -1
        while len(queue) > 0:
            next_node = queue.pop()
            if self.nodes[next_node].finish:
                cur_node = next_node
                answer = set([cur_node])
                while came_from[cur_node] != -1:
                    cur_node = came_from[cur_node]
                    answer.add(cur_node)
                return answer, True
            for e in self.nodes[next_node].edges:
                n = self.edges[e].index_to
                if not n in used:
                    used.add(n)
                    queue.append(n)
                    came_from[n] = next_node
        return used, False

    def is_finished(self):
        return self.nodes[self.current_node].finish

    def goto(self, c):
        for e in self.nodes[self.current_node].edges:
            if self.edges[e].letter == c:
                self.current_node = self.edges[e].index_to
                return self.edges[e].index
        raise AutomateNoWayException()

    def check_word(self, word):
        cur_node = self.current_node
        self.current_node = self.start_node
        try:
            for c in word:
                self.goto(c)
            ans = self.is_finished()
            self.current_node = cur_node
            return ans
        except AutomateNoWayException:
            self.current_node = cur_node
            return False

    def reset(self):
        self.current_node = self.start_node

    def __repr__(self):
        result = "Automate:\n"
        result += "Start node:" + str(self.start_node) + ", current active node: " + str(self.current_node) + "\n"
        result += "Nodes:\n"
        for node in self.nodes:
            result += str(node) + " "
        result += "\n"
        result += "Edges:\n"
        for edge in self.edges:
            result += str(edge)
        return result

    def __hash__(self):
        ans = 0
        for edge in self.edges:
            ans += (edge.index + 1) * edge.index_from * edge.index_to * ord(edge.letter)
            ans %= 1_000_000_007
        return ans

