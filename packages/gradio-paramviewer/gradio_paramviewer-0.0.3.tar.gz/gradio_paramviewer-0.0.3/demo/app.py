import gradio as gr
from gradio_paramviewer import ParamViewer
from sample import docs

with gr.Blocks() as demo:
    ParamViewer(
        value=docs,
    )


if __name__ == "__main__":
    demo.launch()
