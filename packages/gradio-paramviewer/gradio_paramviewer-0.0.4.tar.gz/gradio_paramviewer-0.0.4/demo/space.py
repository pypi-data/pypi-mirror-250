
import gradio as gr
from app import demo as app
from gradio_paramviewer import ParamViewer
import os

_docs = {'ParamViewer': {'description': 'Displays an interactive table of parameters and their descriptions and default values width syntax highlighting', 'members': {'__init__': {'value': {'type': 'list[Parameter] | None', 'default': 'None', 'description': 'A list of dictionaries with keys "type", "description", and "default" for each parameter.'}, 'language': {'type': '"python" | "typescript"', 'default': '"python"', 'description': 'The language to display the code in. One of "python" or "typescript".'}, 'linkify': {'type': 'list[str] | None', 'default': 'None', 'description': 'A list of strings to linkify. If a string is found in the description, it will be linked to the corresponding url.'}, 'x': {'type': 'str', 'default': '"100%"', 'description': None}}, 'postprocess': {'value': {'type': 'list[Parameter]', 'default': "<class 'inspect._empty'>", 'description': 'A list of dictionaries with keys "type", "description", and "default" for each parameter.'}, 'return': {'type': 'list[Parameter]', 'description': 'A list of dictionaries with keys "type", "description", and "default" for each parameter.'}}, 'preprocess': {'payload': {'type': 'list[Parameter]', 'default': "<class 'inspect._empty'>", 'description': 'A list of dictionaries with keys "type", "description", and "default" for each parameter.'}, 'value': {'type': 'list[Parameter]', 'default': "<class 'inspect._empty'>", 'description': 'A list of dictionaries with keys "type", "description", and "default" for each parameter.'}, 'return': {'type': 'list[Parameter]', 'description': 'A list of dictionaries with keys "type", "description", and "default" for each parameter.'}}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the ParamViewer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the ParamViewer.'}}}, '__meta__': {'additional_interfaces': {'Parameter': {'source': 'class Parameter(TypedDict):\n    type: str\n    description: ParameterOne\n    default: ParameterTwo\n', 'refs': ['ParameterOne', 'ParameterTwo']}, 'ParameterOne': {'source': 'class ParameterOne(TypedDict):\n    type: str\n    description: str\n    default: ParameterTwo\n', 'refs': ['ParameterTwo']}, 'ParameterTwo': {'source': 'class ParameterTwo(TypedDict):\n    type: str\n    description: str\n    default: ParameterThree\n', 'refs': ['ParameterThree']}, 'ParameterThree': {'source': 'class ParameterThree(TypedDict):\n    type: str\n    description: str\n    default: str\n'}}, 'user_fn_refs': {'ParamViewer': ['Parameter']}}}
    
abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_paramviewer`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_paramviewer/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_paramviewer"></a><a href="https://github.com/pngwn/gradio-paramviewer/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a>None
</div>

A gradio component that renders a pretty table for python or javascript function or method parameters.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_paramviewer
```

## Usage

```python
import gradio as gr
from gradio_paramviewer import ParamViewer
from sample import docs

with gr.Blocks() as demo:
    ParamViewer(
        value=docs,
    )


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `ParamViewer`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    ParamViewer(value=_docs["ParamViewer"]["members"]["__init__"], linkify=['Parameter'])


    gr.Markdown("### Events")
    ParamViewer(value=_docs["ParamViewer"]["events"], linkify=['Event'])



    gr.Markdown("""

### User function



- **As output:** Is passed, A list of dictionaries with keys "type", "description", and "default" for each parameter..
- **As input:** Should return, A list of dictionaries with keys "type", "description", and "default" for each parameter..

```python
def predict(
    value: list[Parameter]
) -> list[Parameter]:
    return value 
```
""", elem_classes=["md-custom", "ParamViewer-user-fn"], header_links=True)


    


    code_Parameter = gr.Markdown("""
## `Parameter`
```python
class Parameter(TypedDict):
    type: str
    description: ParameterOne
    default: ParameterTwo

```""", elem_classes=["md-custom", "Parameter"], header_links=True)

    code_ParameterOne = gr.Markdown("""
## `ParameterOne`
```python
class ParameterOne(TypedDict):
    type: str
    description: str
    default: ParameterTwo

```""", elem_classes=["md-custom", "ParameterOne"], header_links=True)

    code_ParameterTwo = gr.Markdown("""
## `ParameterTwo`
```python
class ParameterTwo(TypedDict):
    type: str
    description: str
    default: ParameterThree

```""", elem_classes=["md-custom", "ParameterTwo"], header_links=True)

    code_ParameterThree = gr.Markdown("""
## `ParameterThree`
```python
class ParameterThree(TypedDict):
    type: str
    description: str
    default: str

```""", elem_classes=["md-custom", "ParameterThree"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
        Parameter: ['ParameterOne', 'ParameterTwo'], 
        ParameterOne: ['ParameterTwo'], 
        ParameterTwo: ['ParameterThree'], 
        ParameterThree: [], };
    const user_fn_refs = {
        ParamViewer: ['Parameter'], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
        
        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()



