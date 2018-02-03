#########################################################
# Author: Shubhakar R Tipireddy
# Steps to execute:
    # python johnson.py [graph file in gpickle format]
#########################################################

import networkx as nx
import sys

def initialize(stack, blocked, block_map, nodes_list):
    stack = []
    for node in nodes_list:
        blocked[node] = False
        block_map[node] = []

def current_cycle():
    return stack + [start_node]

def CIRCUIT(node, component):
    loop_found = False
    assert node not in stack
    stack.append(node)
    blocked[node] = True

    for n in component.neighbors(node):
        if start_node == n:
            print >> fcycles, current_cycle()
            loop_found = True
        elif not blocked[n]:
            if CIRCUIT(n, component):
                loop_found = True
    if loop_found:
        prev = block_map[node]
        unblock(node)
        assert block_map[node] == []
    else:
        for n in component.neighbors(node):
            if node not in block_map[n]:
                block_map[n].append(node)
    x = stack.pop()
    assert x == node
    return loop_found

def subgraph(nodes):
    return layout_graph.subgraph(nodes)

def LV_SCC(least_node, directed_graph):
    SCCs = nx.strongly_connected_components(directed_graph)
    for scc in SCCs:
        if least_node in scc:
            return subgraph(scc)

def unblock(node):
    blocked[node] = False
    for n in block_map[node]:
        if blocked[n]:
            unblock(n)
            assert block_map[n] == []
        block_map[node] = []

if __name__ == '__main__':
    layout_graph = nx.read_gexf(sys.argv[1])
    for n in c_nodes:
        layout_graph.remove_node(n)
    stack = []
    blocked = {}
    block_map = {}
    fcycles = open("layout_graph_cycles.txt", 'w')

    nodes = list(layout_graph.nodes())
    sorted_nodes = sorted(nodes, key=int)
    #sys.setrecursionlimit(len(sorted_nodes))

    while len(sorted_nodes) != 0:
        start_node = sorted_nodes[0]
        curr_component = LV_SCC(start_node, subgraph(sorted_nodes))
        if len(curr_component.nodes()) != 0:
            CC_nodes = sorted(list(curr_component.nodes()), key=int)
            assert CC_nodes[0] == start_node
            initialize(stack, blocked, block_map, CC_nodes)
            status = CIRCUIT(start_node, curr_component)
            if not status:
                print "no cycle found with node:", start_node
            del sorted_nodes[0]
        else:
            break
    fcycles.close()
