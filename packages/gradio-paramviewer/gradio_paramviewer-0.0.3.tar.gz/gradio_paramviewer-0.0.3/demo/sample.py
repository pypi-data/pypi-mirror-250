docs = {
    "width": {
        "default": "None\n",
        "type": "int | None\n",
        "description": "Width of the displayed image in pixels.",
    },
    "type": {
        "default": '"numpy"\n',
        "type": '"numpy" | "pil" | "filepath"\n',
        "description": 'The format the image is converted to before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image.',
    },
}
