# Huffman Tree Generator and Encoder/Decoder

This is a Python code that generates a Huffman tree and performs encoding and decoding operations on text using the generated tree. `tkinter` is used to create the GUI. The following dependencies are required:

- graphviz==0.20.1
- Pillow==9.5.0
- tk==0.1.0

You can install these dependencies by running the following command:

## Usage

1. Make sure you have the required dependencies installed.
2. Run the script using `python3 huffman.py`.

### Encoding

1. Enter the text you want to encode in the "Enter text to encode" text box.
2. Click the "Encode" button to generate the Huffman tree and encode the text.
3. The encoded text will be displayed in the "Encoded text" text box.
4. A visualization of the Huffman tree will be shown in the canvas area.

### Decoding

1. Enter the encoded text in the "Encoded text" text box.
2. Click the "Decode" button to decode the text using the generated Huffman tree.
3. The decoded text will be displayed in the "Decoded text" text box.

## Code Explanation

The `HuffmanNode` class represents nodes in the Huffman tree. The `build_huffman_tree` function constructs the Huffman tree based on the input text.

The `create_huffman_graph` function generates a graph representation of the Huffman tree using the `graphviz` library.

The `render_huffman_graph` function renders the Huffman tree graph as an image and displays it in the GUI.

The `on_encode_button_click` function is called when the "Encode" button is clicked and performs the encoding operation. It builds the Huffman tree, generates Huffman codes for each character in the tree using the `build_huffman_codes` function, encodes the input text using the Huffman codes, and visualizes the Huffman tree using the `render_huffman_graph` function.

The `on_decode_button_click` function is called when the "Decode" button is clicked and performs the decoding operation. It decodes the encoded text using the Huffman tree generated from the input text.

## Demo

<img src="https://s11.gifyu.com/images/SuqFQ.gif" alt="Demo GIF" style="height: 500px;">
