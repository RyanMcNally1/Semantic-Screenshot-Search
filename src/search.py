from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import json

def transform(model, sentence):
    embedding = model.encode(sentence)
    return embedding

def load_index():
    with open("index.json", "r") as file:
        index = json.load(file)
    return index

def search_images(model, index, query_embedding):
    for record in index:
        record["embedding"] = transform(model, record["text"])
        record["score"] = util.cos_sim(query_embedding, record["embedding"]).item()
        print(f"{record["filename"]} score: {record["score"]:.4f}")

def main():
    transformer = SentenceTransformer("all-MiniLM-L6-v2")

    image_index = load_index()
    user_sentence = input("Input search query: ").strip()
    input_embedding = transform(transformer, user_sentence)

    search_images(transformer, image_index, input_embedding)

if __name__ == "__main__":
    main()