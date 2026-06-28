
Goal:
Create a Machine Learning model to detect if a text is AI generated or not. The model should output a 1 to 100 score of how ai generated the text given to it is. 0 means text with almost no chance of being ai generated and 100% means almost certainly the text is ai generated text. 


Abstract of the approach to achieving the goal: 
The short abstract of how it works is that we train a model using a dataset of ai vs human generated text using an entire array of text metrics as parameters. 

The implementation is described in the paper ai_generated_mll_predictor.pdf. 

The implementation in the paper uses the following software. Please implement it with this software. And it also uses a kaggle dataset which is obtainable using:

```
import kagglehub

# Download latest version
path = kagglehub.dataset_download("shanegerami/ai-vs-human-text")

print("Path to dataset files:", path)
```



spaCy

spaCy is a library for advanced Natural Language Processing in Python and Cython. It's built on the very latest research, and was designed from day one to be used in real products.
https://github.com/explosion/spaCy


TextDescriptives
A Python library for calculating a large variety of metrics from text(s) using spaCy v.3 pipeline components and extensions.

https://github.com/HLasse/textdescriptives

