import pickle
import faiss
import numpy as np
import os

def load_model_index_and_filenames(model_path, faiss_index_path, filenames_path):
    """
    Loads the model, FAISS index, and filenames from specified paths.

    Args:
    model_path (str): Path to the saved model.
    faiss_index_path (str): Path to the saved FAISS index.
    filenames_path (str): Path to the saved filenames.

    Returns:
    tuple: A tuple containing the loaded model, FAISS index, and list of filenames.
    """
    model = pickle.load(open(model_path, "rb"))
    faiss_index = faiss.read_index(faiss_index_path)
    filenames = pickle.load(open(filenames_path, "rb"))
    return model, faiss_index, filenames

def count_occurrences(query, text, exact_search):
    """
    Counts the occurrences of a query in a given text.

    Args:
    query (str): The search query.
    text (str): The text in which to search for the query.
    exact_search (bool): Flag to indicate whether to perform exact or approximate search.

    Returns:
    int: The count of occurrences of the query in the text.
    """
    text = text.lower()
    count = 0

    # Count occurrences based on exact or approximate search
    if exact_search:
        count = text.count(query.lower())
    else:
        for word in query.lower().split():
            count += text.count(word)

    return count

def search(query, model, faiss_index, filenames, text_directory, top_n=5):
    """
    Performs a search on the indexed data using a query.

    Args:
    query (str): The search query.
    model: The Doc2Vec model.
    faiss_index: The FAISS index.
    filenames (list): List of filenames corresponding to the documents in the index.
    text_directory (str): Directory where the text files are stored.
    top_n (int, optional): Number of top results to return. Defaults to 5.

    Returns:
    list: A list of search results with filename, distance, snippet, and occurrences.
    """
    # Vectorize the query and search in the FAISS index
    query_vector = model.infer_vector(query.lower().split())
    query_vector = np.array(query_vector).reshape(1, -1).astype('float32')
    distances, indices = faiss_index.search(query_vector, top_n)

    # Determine if the search is exact
    exact_search = query.startswith('"') and query.endswith('"')
    query = query[1:-1].lower() if exact_search else query.lower()

    # Compile search results
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
    """
    Cleans the given text by removing new lines and excessive spaces.

    Args:
    text (str): The text to clean.

    Returns:
    str: The cleaned text.
    """
    # Replace newlines and carriage returns, then remove extra spaces
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    return text

def find_approximate_snippet(query, text, context_size=255):
    """
    Finds an approximate snippet from text based on a query.

    Args:
    query (str): The search query.
    text (str): The text to search within.
    context_size (int, optional): The size of context around the query. Defaults to 255.

    Returns:
    str: A snippet of text around the query.
    """
    # Identify the closest occurrence of any word in the query
    words = query.split()
    closest_start = len(text)
    closest_end = 0

    for word in words:
        start_index = text.find(word)
        if start_index != -1:
            closest_start = min(closest_start, start_index)
            end_index = start_index + len(word)
            closest_end = max(closest_end, end_index)

    # Extract snippet if found
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
    """
    Finds an exact snippet from text based on a query.

    Args:
    query (str): The search query.
    text (str): The text to search within.
    context_size (int, optional): The size of context around the query. Defaults to 255.

    Returns:
    str: A snippet of text around the query.
    """
    # Locate the exact query in the text
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