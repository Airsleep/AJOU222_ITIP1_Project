from zss import simple_distance, Node

tags = ['arithmetic', 'breadth-first search', 'data structures', 'dynamic programming',
        'graph theory', 'graph traversal', 'implementation', 'mathematics', 'sorting', 'string']
mat = [[48, 0, 37, 0, 38, 0, 137, 91, 0, 0],
       [58, 0, 0, 0, 0, 0, 159, 114, 0, 57],
       [39, 0, 0, 0, 0, 0, 145, 106, 0, 55],
       [58, 0, 0, 0, 0, 0, 155, 121, 0, 46],
       [39, 0, 44, 0, 49, 0, 85, 86, 0, 0],
       [42, 0, 0, 0, 49, 0, 124, 88, 42, 40],
       [0, 56, 0, 0, 80, 64, 95, 50, 0, 0],
       [0, 0, 0, 0, 50, 0, 97, 79, 0, 0],
       [0, 0, 0, 36, 0, 0, 88, 103, 0, 0],
       [52, 0, 45, 0, 37, 0, 109, 100, 43, 0]]
mat_with_tags = []

idx = 0
for e in mat:
    mat_with_tags.append([])
    for i in range(len(tags)):
        mat_with_tags[idx].append(0)
    eidx = 0
    for ee in e:
        mat_with_tags[idx][eidx] = [ee, tags[eidx]]
        eidx += 1
    mat_with_tags[idx].sort(key=lambda x: (-x[0], x[1]))
    idx += 1

# for e in mat_with_tags:
#     print(e)

node_iter = 0
tags_len = len(tags)
# print(node_iter)
# print(node_max_cnt)
# print(tags_len)


def make_node(parent_node, child_cnt, mat):
    global node_cnt
    global mat_with_tags
    if node_cnt >= tags_len:
        return parent_node
    else:
        for i in range(child_cnt):
            if node_cnt >= tags_len:
                break
            temp_child_node = Node(mat[node_cnt][1], [])
            parent_node.addkid(temp_child_node)
            node_cnt += 1
            next_child_cnt = child_cnt * 2
            make_node(temp_child_node, next_child_cnt, mat)


nodes = Node('top', [])
node_cnt = 0


ret_node1 = make_node(nodes, 2, mat_with_tags[0])

nodes2 = Node('top', [])
node_cnt = 0

for i in nodes.iter():
    print(i)
    print("-"*40)

ret_node2 = make_node(nodes2, 2, mat_with_tags[3])
ret = simple_distance(nodes, nodes2)
print(ret)

x = Node('a', [Node('b', [Node('c', [Node('d', [Node('e', [])])])])])
y = Node('b', [Node('c', [Node('d', [Node('e', [Node('a', [])])])])])
print("-"*20 + "test")
print(simple_distance(x, y))
