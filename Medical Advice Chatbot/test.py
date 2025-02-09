from langchain.embeddings import HuggingFaceEmbeddings


def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    return embeddings
embeddings = download_hugging_face_embeddings()
print(embeddings)


