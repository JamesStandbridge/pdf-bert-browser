import pickle
import faiss
import numpy as np
import torch
import os

def load_model_index_and_filenames(model_path, tokenizer_path, faiss_index_path, filenames_path):
    """
    Load the tokenizer, model, FAISS index, and filenames from disk.

    Args:
        model_path (str): Path to the saved model.
        tokenizer_path (str): Path to the saved tokenizer.
        faiss_index_path (str): Path to the saved FAISS index.
        filenames_path (str): Path to the saved filenames list.

    Returns:
        tuple: The tokenizer, model, FAISS index, and list of filenames.
    """
    tokenizer = pickle.load(open(tokenizer_path, "rb"))
    model = pickle.load(open(model_path, "rb"))
    faiss_index = faiss.read_index(faiss_index_path)
    filenames = pickle.load(open(filenames_path, "rb"))
    return tokenizer, model, faiss_index, filenames

def count_occurrences(query, text, exact_search):
    """
    Count the occurrences of a query in a text, either as an exact match or 
    as individual keywords.

    Args:
        query (str): The search query.
        text (str): The text to search within.
        exact_search (bool): Whether to perform an exact match search.

    Returns:
        int: The number of occurrences of the query.
    """
    text = text.lower()
    count = 0

    if exact_search:
        count = text.count(query.lower())
    else:
        for word in query.lower().split():
            count += text.count(word)

    return count

def search(query, tokenizer, model, faiss_index, filenames, text_directory, top_n=5):
    """
    Perform a search against a FAISS index using a query.

    Args:
        query (str): The search query.
        tokenizer (Tokenizer): The tokenizer used for processing the query.
        model (Model): The model used to encode the query.
        faiss_index (faiss.IndexFlatL2): The FAISS index to search against.
        filenames (list): The list of filenames corresponding to the FAISS index's entries.
        text_directory (str): Directory containing the text files to extract snippets from.
        top_n (int): Number of top results to return.

    Returns:
        list: A list of tuples containing filename, distance, snippet, and occurrences.
    """
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
        if idx != -1 and idx < len(filenames):
            original_filename = filenames[idx]
            text_filename = os.path.splitext(original_filename)[0] + '.txt'
            with open(os.path.join(text_directory, text_filename), "r") as file:
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
            print(f"Invalid index returned by FAISS: {idx}")
            continue

    return results

def clean_text(text):
    """
    Cleans the input text by removing unwanted characters and whitespace.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    # Replace newlines and carriage returns with space
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Replace multiple spaces with a single space
    text = ' '.join(text.split())
    return text

def find_approximate_snippet(query, text, context_size=255):
    """
    Finds an approximate snippet in the text that matches the query.

    This function searches for the first occurrence of each word in the query
    and returns a snippet from the text surrounding these words.

    Args:
        query (str): The search query with individual words to match.
        text (str): The text to search within.
        context_size (int): The number of characters around the query match to include in the snippet.

    Returns:
        str: A snippet from the text that includes the query words.
    """
    words = query.split()
    closest_start = len(text)
    closest_end = 0

    # Find the position of each word in the query
    for word in words:
        start_index = text.find(word)
        if start_index != -1:
            closest_start = min(closest_start, start_index)
            end_index = start_index + len(word)
            closest_end = max(closest_end, end_index)

    # If words are found, create a snippet
    if closest_start < len(text) and closest_end > 0:
        start_snippet = max(0, closest_start - context_size)
        end_snippet = min(closest_end + context_size, len(text))

        # Find the sentence boundaries for the snippet
        start_sentence = text.rfind('. ', 0, start_snippet) + 2
        if start_sentence < 0:
            start_sentence = 0
        end_sentence = text.find('. ', end_snippet)
        if end_sentence < 0:
            end_sentence = len(text)
        else:
            end_sentence += 2

        # Return the clean snippet
        return clean_text(text[start_sentence:end_sentence])

    # Return a message if no snippet is found
    return "Snippet not found."

def find_snippet(query, text, context_size=255):
    """
    Finds an exact snippet in the text that matches the query.

    Args:
        query (str): The exact search query to match in the text.
        text (str): The text to search within.
        context_size (int): The number of characters around the query match to include in the snippet.

    Returns:
        str: A snippet from the text that exactly matches the query.
    """
    query_length = len(query)
    start_index = text.find(query)

    # If the query is found, create a snippet
    if start_index != -1:
        start_snippet = max(0, start_index - context_size)
        end_snippet = min(start_index + query_length + context_size, len(text))

        # Find the sentence boundaries for the snippet
        start_sentence = text.rfind('. ', 0, start_snippet) + 2
        if start_sentence < 0:
            start_sentence = 0

        end_sentence = text.find('. ', end_snippet)
        if end_sentence < 0:
            end_sentence = len(text)
        else:
            end_sentence += 2

        # Return the clean snippet
        return clean_text(text[start_sentence:end_sentence])

    # Return a message if no snippet is found
    return "Snippet not found."

