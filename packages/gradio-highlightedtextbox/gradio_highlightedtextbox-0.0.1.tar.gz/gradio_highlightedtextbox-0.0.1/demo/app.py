
import gradio as gr
from gradio_highlightedtextbox import HighlightedTextbox

def listify(x):
    return [(x, None)]

demo = gr.Interface(
    lambda x: x,
    gr.Textbox("Hello world!"),
    HighlightedTextbox(),
)

demo.launch()
