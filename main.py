class Node:
    """A class used to represent a Node in the huffman binary tree"""

    def __init__(self, byte: [int, None], frequency: int):
        """Constructor for the Node class"""

        self.byte = byte
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None


def build_tree(input_bytes: bytearray) -> Node:
    """Function to generate the huffman tree

    Parameters
    ----------
    input_bytes: bytearray
       The bytearray to generate the tree
    """

    # Get the frequency per byte
    frequencies = {}
    for byte in input_bytes:
        frequencies[byte] = frequencies.get(byte, 0) + 1

    nodes = [Node(byte, frequencies[byte]) for byte in frequencies]

    while len(nodes) > 1:
        # Sort the nodes from low -> high by frequency
        nodes = sorted(nodes, key=lambda node: node.frequency)

        # Combine the 2 least common nodes to 1 new node
        new_node = Node(None, nodes[0].frequency + nodes[1].frequency)
        new_node.leftChild = nodes[0]
        new_node.rightChild = nodes[1]

        nodes.remove(nodes[0])
        nodes.remove(nodes[0])

        nodes.append(new_node)

    # Return the parent tree node
    return nodes[0]


def get_codes(node: Node) -> dict:
    """Get the codes corresponding to the bytes from the tree

    Parameters
    ----------
    node: Node
       The huffman tree parent Node

    Returns
    -------
    dict
       The dictionary containing the code/byte pairs
    """

    codes = {}

    def get_next_code(node: Node, prefix: str = ''):
        """Recursive function to loop through every node in the tree and add it to the 'codes' dictionary

        Parameters
        ----------
        node: Node
           The tree node
        prefix: str
           The current code of the node
        """

        if node.byte is not None:
            codes[node.byte] = prefix
        else:
            get_next_code(node.leftChild, prefix + '0')
            get_next_code(node.rightChild, prefix + '1')

    get_next_code(node)

    return codes


def dec_to_bin(number: int, bits: int) -> str:
    """Converts an integer to a binary string with a certain bit length

    Parameters
    ----------
    number: int
       The integer to convert
    bits: int
       The amount of bits that can be used

    Returns
    -------
    str
       The binary string
    """

    return ('0' * bits + bin(number)[2:])[-bits:]


def bin_string_to_bytearray(binary_string: str) -> bytearray:
    """Converts a binary string to a bytearray

    Parameters
    ----------
    binary_string: str
       The binary string used to build the bytearray

    Returns
    -------
    bytearray
       The generated bytearray
    """

    # Fill in bits if the binary string is not dividable by 8 (byte)
    binary_string += ((8 - len(binary_string)) % 8) * '0'

    # Generate the bytearray
    bytes_array = bytearray()
    for binary_byte in [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]:
        bytes_array.append(int(binary_byte, 2))

    return bytes_array


def compress_file(input_filename: str, output_filename: str):
    """Function to compress a file with the huffman algorithm

    Arguments
    ---------
    input_filename: str
       The name of the file to convert
    output_filename: str
       The name of the file to store the compressed data
    """

    with open(input_filename, 'rb') as input_file:
        input_bytes = bytearray(input_file.read())
        output_binary_string = ''

        # If the file is not empty
        if len(input_bytes) > 0:
            # Build the tree and get the codes from the tree
            tree = build_tree(input_bytes)
            codes = get_codes(tree)

            # Transform the bytes to their corresponding codes
            output = "".join([codes[byte] for byte in input_bytes])

            # Get the length of the code lengths. More information can be found in the README file
            max_code_length_length = len(bin(max(map(lambda code: len(code), codes.values())))) - 2

            # Write the amount of codes
            output_binary_string += dec_to_bin(len(codes), 8)
            # Write the length of the code length
            # (minus 1 because the length cannot be 0 and so we have the possibility to save 1 byte)
            output_binary_string += dec_to_bin(max_code_length_length - 1, 8)

            # Write all the codes to the output
            for i, (byte, code) in enumerate(codes.items()):
                # Write the byte
                output_binary_string += dec_to_bin(byte, 8)
                # Write the length of the code
                output_binary_string += dec_to_bin(len(code), max_code_length_length)
                # Write the code itself
                output_binary_string += code

            # Write the length of the filler byte
            output_binary_string += dec_to_bin((len(output_binary_string) + len(output) + 3) % 8, 3)
            # Write the actual compressed data
            output_binary_string += output

        # Save the output to the file
        with open(output_filename, 'wb+') as output_file:
            output_file.write(bin_string_to_bytearray(output_binary_string))


def decompress_file(input_filename: str, output_filename: str):
    """Function to decompress a file which is compressed by the huffman algorithm

    Arguments
    ---------
    input_filename: str
       The name of the compressed file to decompress
    output_filename: str
       The name of the file to store the decompressed data
    """

    with open(input_filename, 'rb') as input_file:
        # Read the file and convert the bytes to binary strings
        input_bytes = "".join([dec_to_bin(byte, 8) for byte in bytearray(input_file.read())])
        output_binary_string = ''

        # If the file is not empty
        if len(input_bytes) > 0:
            # Get the amount of codes
            amount_of_codes = int(input_bytes[0:8], 2)
            # Get the length of the length of a code
            # Plus one, reason is explained at line 159
            code_length_length = int(input_bytes[8:16], 2) + 1
            input_bytes = input_bytes[16:]

            # Get the codes
            codes = {}
            for i in range(amount_of_codes):
                # Get the length of the code
                code_length = int(input_bytes[8:8 + code_length_length], 2)
                code_offset = 8 + code_length_length
                # Get the byte
                codes[input_bytes[code_offset:code_offset + code_length]] = input_bytes[0:8]
                # Get the code corresponding to the byte
                input_bytes = input_bytes[code_offset + code_length:]

            # Get the length of the filler bits
            filler_bits_length = int(input_bytes[:3], 2)
            input_bytes = input_bytes[3:]

            # Convert the compressed data to the bytes
            buffer = ''
            for bit in [input_bytes[i] for i in range(len(input_bytes) - filler_bits_length)]:
                # Add the bit to the buffer
                buffer += bit
                # If the buffer equals to a code, add it to the output and reset the buffer
                if buffer in codes:
                    output_binary_string += codes[buffer]
                    buffer = ''

        # Save the output to the file
        with open(output_filename, 'wb+') as output_file:
            output_file.write(bin_string_to_bytearray(output_binary_string))


if __name__ == '__main__':
    compress_file('lorem-ipsum', 'lorem-ipsum-compressed')
    decompress_file('lorem-ipsum-compressed', 'lorem-ipsum-decompressed')
