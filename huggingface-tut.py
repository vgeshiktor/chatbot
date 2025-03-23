from typing import Any
from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification, AutoTokenizer)
import torch
import tensorflow as tf

dataset = load_dataset("glue", "mrpc", split="train")

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


def encode(examples: Any) -> Any:
    return tokenizer(
        examples["sentence1"],
        examples["sentence2"],
        truncation=True,
        padding="max_length",
    )


dataset = dataset.map(encode, batched=True)
print(dataset)

dataset = dataset.map(lambda examples: {
    "labels": examples["label"]}, batched=True)

dataset.set_format(
    type="torch", columns=[
        "input_ids", "token_type_ids", "attention_mask", "labels"]
)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)

tf_dataset = model.prepare_tf_dataset(
    dataset,
    batch_size=4,
    shuffle=True,
)
