#search.py

import pickle
import faiss
import numpy as np
import torch

import os
from sklearn.metrics.pairwise import cosine_similarity

# Fonction pour calculer la similarité cosinus
def semantic_similarity(vector1, vector2):
    return cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]

# Fonction pour diviser le texte en segments plus grands
def get_text_segments(text, segment_length=300):
    words = text.split()
    for i in range(0, len(words), segment_length):
        yield ' '.join(words[i:i+segment_length])

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

def find_exact_phrase(phrase, text):
    """Trouver une phrase exacte dans le texte."""
    start_index = text.find(phrase)
    if start_index != -1:
        end_index = start_index + len(phrase)
        return text[start_index:end_index]  # Retourne la phrase exacte
    return "Phrase not found."


def search(query, tokenizer, model, faiss_index, filenames, text_directory, top_n=5, max_documents=10):
    # Tokenize et encode la requête
    tokenized_query = tokenizer.encode(query, add_special_tokens=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(input_ids=tokenized_query)
    query_vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    # Utiliser FAISS pour trouver les vecteurs de document les plus proches
    query_vector = np.array(query_vector).reshape(1, -1).astype('float32')
    distances, indices = faiss_index.search(query_vector, top_n)

    # Process the search results
    results = []
    for idx, distance in zip(indices[0][:max_documents], distances[0][:max_documents]):
        if idx != -1 and idx < len(filenames):
            original_filename = filenames[idx]
            text_filename = os.path.splitext(original_filename)[0] + '.txt'
            with open(f"{text_directory}/{text_filename}", "r") as file:
                text = file.read().lower()

            # Mise en cache des vecteurs de segments
            segment_vectors = {}
            best_snippet = ""
            highest_similarity = 0

            # Analyser chaque segment
            for segment in get_text_segments(text):
                if segment in segment_vectors:
                    segment_vector = segment_vectors[segment]
                else:
                    tokenized_segment = tokenizer.encode(segment, add_special_tokens=True, return_tensors="pt")
                    with torch.no_grad():
                        segment_output = model(input_ids=tokenized_segment)
                    segment_vector = segment_output.last_hidden_state.mean(dim=1).squeeze().numpy()
                    segment_vectors[segment] = segment_vector

                similarity = semantic_similarity(query_vector, segment_vector)
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_snippet = segment

            results.append((original_filename, distance, best_snippet, highest_similarity))
        else:
            print(f"Indice invalide retourné par FAISS: {idx}")
            continue
    
    return results


def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text

def find_approximate_snippet(query, text, context_size=255):
    words = query.split()
    word_positions = {word: [] for word in words}

    # Trouver les positions de chaque mot dans le texte
    for word in words:
        start = 0
        while start < len(text):
            start = text.find(word, start)
            if start == -1:
                break
            word_positions[word].append(start)
            start += len(word)

    # Trouver le meilleur snippet basé sur la proximité des mots
    best_snippet = ""
    min_distance = float('inf')
    for start_pos in word_positions[words[0]]:  # Commencer par le premier mot
        end_pos = start_pos
        current_distance = 0

        for word in words[1:]:
            closest_pos = min(word_positions[word], key=lambda pos: abs(pos - end_pos))
            current_distance += abs(closest_pos - end_pos)
            end_pos = closest_pos

        if current_distance < min_distance:
            min_distance = current_distance
            snippet_start = max(0, start_pos - context_size)
            snippet_end = min(end_pos + context_size, len(text))
            best_snippet = clean_text(text[snippet_start:snippet_end])

    return best_snippet if best_snippet else "Snippet not found."


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

