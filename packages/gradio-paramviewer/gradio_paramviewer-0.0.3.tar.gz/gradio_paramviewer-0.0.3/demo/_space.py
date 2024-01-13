import gradio as gr

from app import demo as app
from gradio_paramviewer import ParamViewer
import os


_docs = {
    "ParamViewer": {
        "description": "Displays an interactive table of parameters and their descriptions and default values width syntax highlighting",
        "members": {
            "__init__": {
                "value": {
                    "type": "list[Parameter]\n",
                    "default": "None\n",
                    "description": 'A list of dictionaries with keys "type", "description", and "default" for each parameter.',
                },
                "language": {
                    "type": '"python" | "typescript"\n',
                    "default": '"python"\n',
                    "description": 'The language to display the code in. One of "python" or "typescript".',
                },
            },
            "postprocess": {"type": "list\n", "return": "list\n"},
            "preprocess": {"type": "list\n", "return": "list\n"},
        },
        "__meta__": {
            "additional_interfaces": {
                "Parameter": "class Parameter(TypedDict):\n    type: str\n    description: str\n    default: str\n"
            }
        },
    }
}

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



A gradio component that renders a pretty table for python or javascript function or method parameters.
    
## Demo""",
        elem_id="start",
        header_links=True,
    )
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
    gr.Markdown("## ParamViewer")
    ParamViewer(
        value=docs,
    )


if __name__ == "__main__":
    demo.launch()

```

---


## `ParamViewer`
### Initialization
""",
        elem_classes=["md-custom"],
        header_links=True,
    )
    ParamViewer(
        value=_docs["ParamViewer"]["members"]["__init__"], linkify=["Parameter"]
    )

    gr.Markdown(
        """
### User function

- **As output:** Is passed a list of dictionaries with keys `"type"`, `"description"`, and `"default"` for each parameter.
- **As input:** Should return a list of dictionaries with keys `"type"`, `"description"`, and `"default"` for each parameter.


```python
def predict(
    value: list[Parameter]
) -> list[Parameter]:
    return value 
```

---


## `Parameter`

```python
class Parameter(TypedDict):
    type: str
    description: str
    default: str
```""",
        elem_classes=["md-custom"],
        header_links=True,
    )
demo.launch()
