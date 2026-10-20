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

def prepare_embeddings(model, index):
    for record in index:
        record["embedding"] = transform(model, record["text"])
    return index

def search_images(index, query_embedding):
    for record in index:
        record["score"] = util.cos_sim(query_embedding, record["embedding"]).item()

    scored = sorted(
    index,
    key=lambda record: record["score"],
    reverse=True
    )

    for record in scored[:5]:
        print(f"{record["filename"]} - {record["score"]:.4f}")


def main():
    transformer = SentenceTransformer("all-MiniLM-L6-v2")
    image_index = load_index()
    embedded_index = prepare_embeddings(transformer, image_index)

    while True:
        user_sentence = input("Type quit to exit\nInput search query: ").strip()
        if user_sentence == "quit":
            print("Exiting program...")
            break
        input_embedding = transform(transformer, user_sentence)
        search_images(embedded_index, input_embedding)

if __name__ == "__main__":
    main()