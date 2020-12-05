class Node:
    def __init__(self, byte: [int, None], frequency: int):
        self.byte = byte
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None


def build_tree(input_bytes: bytearray) -> Node:
    frequencies = {}

    for byte in input_bytes:
        frequencies[byte] = frequencies.get(byte, 0) + 1

    nodes = [Node(byte, frequencies[byte]) for byte in frequencies]

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

    def get_next_code(node: Node, prefix: str = ''):
        if node.byte is not None:
            codes[node.byte] = prefix
        else:
            get_next_code(node.leftChild, prefix + '0')
            get_next_code(node.rightChild, prefix + '1')

    get_next_code(node)

    return codes


def dec_to_bin(number: int, bits: int) -> str:
    return ('0' * bits + bin(number)[2:])[-bits:]


def bin_string_to_bytearray(binary_string: str) -> bytearray:
    binary_string += ((8 - len(binary_string)) % 8) * '0'

    bytes_array = bytearray()
    for binary_byte in [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]:
        bytes_array.append(int(binary_byte, 2))

    return bytes_array


def compress_file(input_filename: str, output_filename: str):
    with open(input_filename, 'rb') as input_file:
        input_bytes = bytearray(input_file.read())

        tree = build_tree(input_bytes)
        codes = get_codes(tree)

        output = "".join([codes[byte] for byte in input_bytes])

        max_code_length_length = len(bin(max(map(lambda code: len(code), codes.values())))) - 2

        output_binary = [dec_to_bin(len(codes), 8), dec_to_bin(max_code_length_length + 1, 8)]

        for i, (byte, code) in enumerate(codes.items()):
            output_binary.append(dec_to_bin(byte, 8))
            output_binary.append(dec_to_bin(len(code), max_code_length_length))
            output_binary.append(code)

        output_binary.append(dec_to_bin((len("".join(output_binary)) + len(output) + 3) % 8, 3))
        output_binary.append(output)

        with open(output_filename, 'wb+') as output_file:
            output_file.write(bin_string_to_bytearray("".join(output_binary)))


def decompress_file(input_filename: str, output_filename: str):
    with open(input_filename, 'rb') as input_file:
        input_bytes = "".join([dec_to_bin(byte, 8) for byte in bytearray(input_file.read())])

        amount_of_codes = int(input_bytes[0:8], 2)
        code_length_length = int(input_bytes[8:16], 2) - 1
        input_bytes = input_bytes[16:]

        codes = {}
        for i in range(amount_of_codes):
            code_length = int(input_bytes[8:8 + code_length_length], 2)
            code_offset = 8 + code_length_length
            codes[input_bytes[code_offset:code_offset + code_length]] = input_bytes[0:8]
            input_bytes = input_bytes[code_offset + code_length:]

        filler_bits_length = int(input_bytes[:3], 2)
        input_bytes = input_bytes[3:]

        output = ''
        buffer = ''
        for bit in [input_bytes[i] for i in range(len(input_bytes) - filler_bits_length)]:
            buffer += bit
            if buffer in codes:
                output += codes[buffer]
                buffer = ''

        with open(output_filename, 'wb+') as output_file:
            output_file.write(bin_string_to_bytearray(output))


if __name__ == '__main__':
    compress_file('lorem-ipsum', 'lorem-ipsum-compressed')
    decompress_file('lorem-ipsum-compressed', 'lorem-ipsum-decompressed')
