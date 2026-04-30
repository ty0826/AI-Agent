#langchain_allama
from langchain_ollama import  OllamaLLM

model = OllamaLLM(
    model="qwen3:4b"
)

model.invoke(input="你是谁")