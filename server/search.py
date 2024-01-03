#search.py

import pickle
import faiss
import numpy as np
import torch

import os

def load_model_index_and_filenames(model_path, tokenizer_path, faiss_index_path, filenames_path):
    tokenizer = pickle.load(open(tokenizer_path, "rb"))
    model = pickle.load(open(model_path, "rb"))
    faiss_index = faiss.read_index(faiss_index_path)
    filenames = pickle.load(open(filenames_path, "rb"))
    return tokenizer, model, faiss_index, filenames

def count_occurrences(query, text, exact_search):
    text = text.lower()
    count = 0

    if exact_search:
        count = text.count(query.lower())
    else:
        for word in query.lower().split():
            count += text.count(word)

    return count


def search(query, tokenizer, model, faiss_index, filenames, text_directory, top_n=5):
    # Tokenize and encode the query
    tokenized_query = tokenizer.encode(query, add_special_tokens=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(input_ids=tokenized_query)
    query_vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    # Use FAISS to find the closest document vectors
    query_vector = np.array(query_vector).reshape(1, -1).astype('float32')
    distances, indices = faiss_index.search(query_vector, top_n)

    # Process the search results
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        if idx != -1 and idx < len(filenames):  # Ajouter une vérification ici
            original_filename = filenames[idx]
            text_filename = os.path.splitext(original_filename)[0] + '.txt'
            with open(f"{text_directory}/{text_filename}", "r") as file:
                text = file.read().lower()
                exact_search = query.startswith('"') and query.endswith('"')
                if exact_search:
                    refined_query = query[1:-1].lower()
                    snippet = find_snippet(refined_query, text)
                    occurrences = count_occurrences(refined_query, text, True)
                else:
                    snippet = find_approximate_snippet(query.lower(), text)
                    occurrences = count_occurrences(query.lower(), text, False)
                results.append((original_filename, distance, snippet, occurrences))
        else:
            # Gérer le cas où l'indice n'est pas valide
            print(f"Indice invalide retourné par FAISS: {idx}")
            continue

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

