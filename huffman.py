import tkinter as tk
import heapq
from collections import defaultdict
from tkinter import messagebox
import graphviz
from PIL import ImageTk, Image

encode_label = None
graph_generated = False

class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq_dict = defaultdict(int)
    for char in text:
        freq_dict[char] += 1

    min_heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(min_heap, HuffmanNode(char, freq))

    while len(min_heap) > 1:
        left_node = heapq.heappop(min_heap)
        right_node = heapq.heappop(min_heap)
        merged_freq = left_node.freq + right_node.freq
        merged_node = HuffmanNode(None, merged_freq, left_node, right_node)
        heapq.heappush(min_heap, merged_node)

    return heapq.heappop(min_heap)


def create_huffman_graph(root):
    graph = graphviz.Graph(format='png')

    def traverse(node, parent_id=None, edge_label=None):
        if node.char:
            graph.node(str(id(node)), label=f"{node.char}:{node.freq}")
        else:
            graph.node(str(id(node)), label=f"{node.freq}")

        if parent_id is not None:
            graph.edge(str(parent_id), str(id(node)), label=edge_label)

        if node.left:
            traverse(node.left, id(node), "0")
        if node.right:
            traverse(node.right, id(node), "1")

    traverse(root)
    return graph

def render_huffman_graph(graph):
    global graph_generated
    graph.render("huffman_tree", format='png', view=False)
    img = Image.open("huffman_tree.png")
    img = img.resize((400, 400), resample=Image.LANCZOS)
    img = img.convert("RGBA")
    white_background = Image.new("RGBA", img.size, (255, 255, 255))
    img_without_alpha = Image.alpha_composite(white_background, img)
    img_without_alpha = img_without_alpha.convert("RGB")
    img_without_alpha = img_without_alpha.resize((400, 400), resample=Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_without_alpha)
    graph_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    graph_canvas.image = img_tk

    graph_generated = True

    if encode_label:
        encode_label.lift(aboveThis=None)


def on_encode_button_click():
    global graph_generated
    global encode_label  
    text = text_entry.get("1.0", "end-1c")
    if text:
        encode_label.destroy()
        huffman_tree = build_huffman_tree(text)
        huffman_codes = build_huffman_codes(huffman_tree)
        encoded_text = encode_text(text, huffman_codes)
        encoded_text_entry.delete("1.0", "end")
        encoded_text_entry.insert("end", encoded_text)
        huffman_graph = create_huffman_graph(huffman_tree)
        render_huffman_graph(huffman_graph)

        if encode_label:
            encode_label.place_forget()
            encode_label.lift() 
    else:
        messagebox.showwarning(
            "Empty Input", "Please enter some text to encode.")

def build_huffman_codes(root):
    codes = {}

    def traverse(node, code):
        if node.char:
            codes[node.char] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")

    traverse(root, "")
    return codes


def encode_text(text, codes):
    encoded_text = ""
    for char in text:
        encoded_text += codes[char]
    return encoded_text


def decode_text(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char:
            decoded_text += current_node.char
            current_node = root

    return decoded_text


def on_decode_button_click():
    encoded_text = encoded_text_entry.get("1.0", "end-1c")
    if encoded_text:
        huffman_tree = build_huffman_tree(text_entry.get("1.0", "end-1c"))
        decoded_text = decode_text(encoded_text, huffman_tree)
        decoded_text_entry.delete("1.0", "end")
        decoded_text_entry.insert("end", decoded_text)
    else:
        messagebox.showwarning(
            "Empty Input", "Please enter some text to decode.")


root = tk.Tk()
root.title("Huffman Tree Generator and Encoder/Decoder")

title_label = tk.Label(root, text="Huffman Tree Generator", font=("Arial", 16, "bold"))
title_label.pack()

outer_frame = tk.Frame(root, padx=10, pady=10)
outer_frame.pack()

graph_canvas = tk.Canvas(outer_frame, width=400, height=400, bg="grey")
graph_canvas.pack()

text_label = tk.Label(root, text="Enter text to encode:")
text_label.pack()
text_entry = tk.Text(root, height=5, width=40)
text_entry.pack()

encode_button = tk.Button(root, text="Encode", command=on_encode_button_click)
encode_button.pack()

encoded_text_label = tk.Label(root, text="Encoded text:")
encoded_text_label.pack()
encoded_text_entry = tk.Text(root, height=5, width=40)
encoded_text_entry.pack()

decode_button = tk.Button(root, text="Decode", command=on_decode_button_click)
decode_button.pack()

decoded_text_label = tk.Label(root, text="Decoded text:")
decoded_text_label.pack()
decoded_text_entry = tk.Text(root, height=5, width=40)
decoded_text_entry.pack()

encode_label = tk.Label(
    outer_frame, text="Encode a string to generate the tree", font=("Arial", 14), bg="grey", fg="black"
)
encode_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
outer_frame.lift()

root.mainloop()
