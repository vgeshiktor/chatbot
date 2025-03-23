from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset

model_name = "openai-community/gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


dataset = load_dataset("PolyAI/minds14", "en-US", split="train")
