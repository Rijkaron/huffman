# Huffman
Huffman coding is a general purpose lossless compression algorithm developed by David A. Huffman ([Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding))

## Installation
This project requires python 3.5+. Install it from [https://www.python.org/downloads](https://www.python.org/downloads/)

## How does it work
I would recommend watching Tom Scott's video on Huffman trees to learn how they work. 

[![How Computers Compress Text: Huffman Coding and Huffman Trees](http://img.youtube.com/vi/JsTptu56GM8/0.jpg)](https://youtu.be/JsTptu56GM8)

### Compressed file layout
The compressed Huffman files are structured as follows (format is {name|size of the value in bits}):
```
{amount_of_codes|8} -> The amount of codes 
{length_of_code_length|8} -> The length of the value with the length of the code
for every code:
  {byte|8} -> 
  {length_of_code|length_of_code_length bits}
  {code|length_of_code} -> The byte,
{length_of_the_filler_bits|3} -> The amount of bits that are used to fill the last byte and shouldn't be read when decompressing
{compressed_data|unknown} -> The actual compressed data
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
