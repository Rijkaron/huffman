class Node:
    def __init__(self, byte, frequency):
        self.byte = byte
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None


def build_tree(input_bytes: bytes):
    frequencies = {}

    for byte in input_bytes:
        frequencies[byte] = frequencies.get(byte, 0) + 1

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


def get_codes(node: Node) -> dict:
    codes = {}

    def get_next_code(node: Node, prefix=''):
        if node.byte is not None:
            codes[node.byte] = prefix
        else:
            get_next_code(node.leftChild, prefix + '0')
            get_next_code(node.rightChild, prefix + '1')

    get_next_code(node)

    return codes


if __name__ == '__main__':
    input_bytes = bytes("huffman was een slimme man", 'utf-8')

    tree = build_tree(input_bytes)
    codes = get_codes(tree)

    result = "".join([codes[letter] for letter in input_bytes])

    print('input:', input_bytes)
    print('codes:', codes)
    print('result:', result)
    print('verschil in bits (zonder tree):', len(input_bytes) * 8 - len(result))
