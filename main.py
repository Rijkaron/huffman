class Node:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None


def build_tree(text):
    frequencies = {}

    for letter in text:
        frequencies[letter] = frequencies.get(letter, 0) + 1

    nodes = [Node(letter, frequencies[letter]) for letter in frequencies]

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda node: node.frequency)

        new_node = Node(None, nodes[0].frequency + nodes[1].frequency)
        new_node.leftChild = nodes[0]
        new_node.rightChild = nodes[1]

        nodes.remove(nodes[0])
        nodes.remove(nodes[0])

        nodes.append(new_node)

    return nodes[0]


def get_codes(node):
    codes = {}

    def get_next_code(node, prefix=''):
        if node.character is not None:
            codes[node.character] = prefix
        else:
            get_next_code(node.leftChild, prefix + '0')
            get_next_code(node.rightChild, prefix + '1')

    get_next_code(node)

    return codes


if __name__ == '__main__':
    text = "huffman was een slimme man"

    tree = build_tree(text)
    codes = get_codes(tree)

    result = "".join([codes[letter] for letter in text])

    print('input:', text)
    print('codes:', codes)
    print('result:', result)
    print('verschil in bits (zonder tree):', len(text) * 8 - len(result))
