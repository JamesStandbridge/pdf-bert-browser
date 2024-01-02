#search.py

import pickle
import faiss
import numpy as np
import os

def load_model_index_and_filenames(model_path, faiss_index_path, filenames_path):
    model = pickle.load(open(model_path, "rb"))
    faiss_index = faiss.read_index(faiss_index_path)
    filenames = pickle.load(open(filenames_path, "rb"))
    return model, faiss_index, filenames

def count_occurrences(query, text, exact_search):
    text = text.lower()
    count = 0

    if exact_search:
        count = text.count(query.lower())
    else:
        for word in query.lower().split():
            count += text.count(word)

    return count


def search(query, model, faiss_index, filenames, text_directory, top_n=5):
    query_vector = model.infer_vector(query.lower().split())
    query_vector = np.array(query_vector).reshape(1, -1).astype('float32')
    distances, indices = faiss_index.search(query_vector, top_n)

    exact_search = query.startswith('"') and query.endswith('"')
    if exact_search:
        query = query[1:-1].lower()
    else:
        query = query.lower()

    results = []
    for idx, distance in zip(indices[0], distances[0]):
        if idx != -1:
            original_filename = filenames[idx]
            text_filename = os.path.splitext(original_filename)[0] + '.txt'
            with open(f"{text_directory}/{text_filename}", "r") as file:
                text = file.read().lower()
                snippet = find_snippet(query, text) if exact_search else find_approximate_snippet(query, text)
                occurrences = count_occurrences(query, text, exact_search)
            results.append((original_filename, distance, snippet, occurrences))
    return results

def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text

def find_approximate_snippet(query, text, context_size=255):
    words = query.split()
    closest_start = len(text)
    closest_end = 0

    for word in words:
        start_index = text.find(word)
        if start_index != -1:
            closest_start = min(closest_start, start_index)
            end_index = start_index + len(word)
            closest_end = max(closest_end, end_index)

    if closest_start < len(text) and closest_end > 0:
        start_snippet = max(0, closest_start - context_size)
        end_snippet = min(closest_end + context_size, len(text))

        start_sentence = text.rfind('. ', 0, start_snippet) + 2
        if start_sentence < 0:
            start_sentence = 0
        end_sentence = text.find('. ', end_snippet)
        if end_sentence < 0:
            end_sentence = len(text)
        else:
            end_sentence += 2

        return clean_text(text[start_sentence:end_sentence])

    return "Snippet not found."

def find_snippet(query, text, context_size=255):
    query_length = len(query)
    start_index = text.find(query)
    if start_index != -1:
        start_snippet = max(0, start_index - context_size)
        end_snippet = min(start_index + query_length + context_size, len(text))

        start_sentence = text.rfind('. ', 0, start_snippet) + 2
        if start_sentence < 0:
            start_sentence = 0

        end_sentence = text.find('. ', end_snippet)
        if end_sentence < 0:
            end_sentence = len(text)
        else:
            end_sentence += 2

        return clean_text(text[start_sentence:end_sentence])
    return "Snippet not found."

