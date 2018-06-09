"""
Parses the .col files and returns a list of graph nodes and edges
"""


class ParseError(Exception):
    pass


def parse_content(file_content: list):
    nodes = []
    found_p = False
    name = ''
    node_cnt = 0
    edge_cnt = 0

    for line in file_content:
        cmd, *rest = line.split()
        if cmd == 'p' and found_p:
            raise ParseError("found more than one p line: " + line)
        elif cmd == 'p' and not found_p:
            found_p = True
            name, node_cnt_s, edge_cnt_s = rest
            node_cnt = int(node_cnt_s)
            edge_cnt = int(edge_cnt_s)
            for i in range(node_cnt):
                nodes.append([])

        elif cmd == 'e' and not found_p:
            raise ParseError("found edges before p")
        elif cmd == 'e' and found_p:
            [edge_from, edge_to] = rest
            if edge_from == edge_to:
                raise ParseError("loop detected: {} - {}", edge_from, edge_to)
            nodes[int(edge_from) - 1].append(int(edge_to) - 1)
            nodes[int(edge_to) - 1].append(int(edge_from) - 1)

    return name, node_cnt, edge_cnt, nodes


def parse(filename):
    file_content = []

    # print("parsing file", filename)
    with open(filename, 'r') as file:
        for line in file:
            file_content.append(line)

    return parse_content(file_content)
