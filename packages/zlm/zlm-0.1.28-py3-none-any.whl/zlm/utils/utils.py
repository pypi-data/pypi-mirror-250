'''
-----------------------------------------------------------------------
File: utils.py
Creation Time: Dec 6th 2023, 7:09 pm
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import os
import re
import time
import json
import platform
import subprocess
from fpdf import FPDF
from pathlib import Path
from datetime import datetime
OS_SYSTEM = platform.system().lower()


def write_file(file_path, data):
    with open(file_path, "w") as file:
        file.write(data)


def read_file(file_path):
    with open(file_path, "r") as file:
        file_contents = file.read()
    return file_contents


def write_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def read_json(file_path: str):
    with open(file_path) as json_file:
        return json.load(json_file)


def job_doc_name(job_details: dict, output_dir: str = "output", type: str = ""):
    company_name = clean_string(job_details["company_name"])
    job_title = clean_string(job_details["title"])[:15]
    doc_name = "_".join([company_name, job_title])
    doc_dir = os.path.join(output_dir, company_name)
    os.makedirs(doc_dir, exist_ok=True)

    if type == "jd":
        return os.path.join(doc_dir, f"{doc_name}_JD.json")
    elif type == "resume":
        return os.path.join(doc_dir, f"{doc_name}_resume.json")
    elif type == "cv":
        return os.path.join(doc_dir, f"{doc_name}_cv.txt")
    else:
        return os.path.join(doc_dir, f"{doc_name}_")


def clean_string(text: str):
    text = text.title().replace(" ", "").strip()
    text = re.sub(r"[^a-zA-Z0-9]+", "", text)
    return text

def open_file(file: str):
    if OS_SYSTEM == "darwin":  # macOS
        os.system(f"open {file}")
    elif OS_SYSTEM == "linux":
        try:
            os.system(f"xdg-open {file}")
        except FileNotFoundError:
            print("Error: xdg-open command not found. Please install xdg-utils.")
    elif OS_SYSTEM == "windows":
        try:
            os.startfile(file)
        except AttributeError:
            print("Error: os.startfile is not available on this platform.")
    else:
        # Default fallback for other systems
        try:
            os.system(f"xdg-open {file}")
        except FileNotFoundError:
            print(f"Error: xdg-open command not found. Please install xdg-utils. Alternatively, open the file manually.")


def save_log(content: any, file_name: str):
    timestamp = int(datetime.timestamp(datetime.now()))
    file_path = f"logs/{file_name}_{timestamp}.txt"
    write_file(file_path, content)


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} took {execution_time:.4f} seconds to execute")
        return result

    return wrapper


def text_to_pdf(text: str, file_path: str):
    """Converts the given text to a PDF and saves it to the specified file path.

    Args:
        text (str): The text to be converted to PDF.
        file_path (str): The file path where the PDF will be saved.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Encode the text explicitly using 'latin-1' encoding
    encoded_text = text.encode('utf-8').decode('latin-1')
    pdf.multi_cell(0, 5, txt=encoded_text)
    pdf.output(file_path)
    # try:
    #     open_file(file_path)
    # except Exception as e:
    #     print("Unable to open the PDF file.")


def save_latex_as_pdf(tex_file_path: str, dst_path: str):
    # Call pdflatex to convert LaTeX to PDF
    prev_loc = os.getcwd()
    os.chdir(os.path.dirname(tex_file_path))
    result = subprocess.run(
        ["pdflatex", tex_file_path, "&>/dev/null"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    os.chdir(prev_loc)
    resulted_pdf_path = tex_file_path.replace(".tex", ".pdf")

    os.rename(resulted_pdf_path, dst_path)

    if result.returncode != 0:
        print("Exit-code not 0, check result!")
    try:
        open_file(dst_path)
    except Exception as e:
        print("Unable to open the PDF file.")

    filename_without_ext = os.path.basename(tex_file_path).split(".")[0]
    unnessary_files = [
        file
        for file in os.listdir(os.path.dirname(os.path.realpath(tex_file_path)))
        if file.startswith(filename_without_ext)
    ]
    for file in unnessary_files:
        file_path = os.path.join(os.path.dirname(tex_file_path), file)
        if os.path.exists(file_path):
            os.remove(file_path)

    with open(dst_path, "rb") as f:
        pdf_data = f.read()

    return pdf_data


def get_default_download_folder():
    """Get the default download folder for the current operating system."""

    if OS_SYSTEM == "windows":
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    elif OS_SYSTEM == "darwin":  # macOS
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    elif OS_SYSTEM == "linux":
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")
    else:
        # Default fallback for other systems
        return os.path.join(str(Path.home()), "Downloads", "JobLLM_Resume_CV")

def parse_json_markdown(json_string: str) -> dict:
    try:
        # Try to find JSON string within first and last triple backticks
        match = re.search(r"""```       # match first occuring triple backticks
                            (?:json)? # zero or one match of string json in non-capturing group
                            (.*)```   # greedy match to last triple backticks""", json_string, flags=re.DOTALL|re.VERBOSE)

        # If no match found, assume the entire string is a JSON string
        if match is None:
            json_str = json_string
        else:
            # If match found, use the content within the backticks
            json_str = match.group(1)

        # Strip whitespace and newlines from the start and end
        json_str = json_str.strip()

        # Parse the JSON string into a Python dictionary while allowing control characters by setting strict to False
        parsed = json.loads(json_str, strict=False)

        return parsed
    except Exception as e:
        print(e)
        return None

def get_prompt(system_prompt_path: str) -> str:
        """
        Reads the content of the file at the given system_prompt_path and returns it as a string.

        Args:
            system_prompt_path (str): The path to the system prompt file.

        Returns:
            str: The content of the file as a string.
        """
        with open(system_prompt_path, encoding="utf-8") as file:
            return file.read().strip() + "\n"


def key_value_chunking(data, prefix=""):
    """Chunk a dictionary or list into key-value pairs.

    Args:
        data (dict or list): The data to chunk.
        prefix (str, optional): The prefix to use for the keys. Defaults to "".

    Returns:
        A list of strings representing the chunked key-value pairs.
    """
    chunks = []
    stop_needed = lambda value: '.' if not isinstance(value, (str, int, float, bool, list)) else ''
    
    if isinstance(data, dict):
        for key, value in data.items():
            if value is not None:
                chunks.extend(key_value_chunking(value, prefix=f"{prefix}{key}{stop_needed(value)}"))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            if value is not None:
                chunks.extend(key_value_chunking(value, prefix=f"{prefix}_{index}{stop_needed(value)}"))
    else:
        if data is not None:
            chunks.append(f"{prefix}: {data}")
    
    return chunks

def remove_urls(list_of_strings):
    """Removes strings containing URLs from a list using regular expressions."""
    filtered_list = [string for string in list_of_strings if not re.search(r"https?://\S+", string)]
    return filtered_list


def jaccard_similarity(doc1, doc2): 
    
    # List the unique words in a document
    words_doc1 = set(doc1.lower().split()) 
    words_doc2 = set(doc2.lower().split())

    # Remove Links and URLs
    words_doc1 = remove_urls(words_doc1)
    words_doc2 = remove_urls(words_doc2)

    # Remove punctuation and special characters: Keep only letters and numbers:
    words_doc1 = set(re.sub(r"[^a-zA-Z0-9]", "", w) for w in words_doc1)
    words_doc2 = set(re.sub(r"[^a-zA-Z0-9]", "", w) for w in words_doc2)

    # Remove empty strings
    words_doc1 = {w for w in words_doc1 if w.strip() != ""}
    words_doc2 = {w for w in words_doc2 if w.strip() != ""} 
    
    # Find the intersection of words list of doc1 & doc2
    intersection = words_doc1.intersection(words_doc2)

    # Find the union of words list of doc1 & doc2
    union = words_doc1.union(words_doc2)
        
    # Calculate Jaccard similarity score 
    jaccard_similarity = float(len(intersection)) / len(union)
    return jaccard_similarity

    # Stemming or Lemmatization (Optional): 
    # Reduce words to root forms: Choose stemming for simpler rules or lemmatization for considering context:
    # from nltk.stem import PorterStemmer
    # stemmer = PorterStemmer()

    # words_doc1 = {stemmer.stem(w) for w in words_doc1}
    # words_doc2 = {stemmer.stem(w) for w in words_doc2}

    # Remove Stop Words: Identify common words: Use a predefined list of stop words to filter out:
    # import nltk
    # nltk.download('stopwords')
    # from nltk.corpus import stopwords

    # stop_words = set(stopwords.words('english'))  # Adjust language as needed

    # words_doc1 = {w for w in words_doc1 if w not in stop_words}
    # words_doc2 = {w for w in words_doc2 if w not in stop_words}

# from deepeval import evaluate
# from deepeval.test_case import LLMTestCase
# from deepeval.metrics import SummarizationMetric

# def get_score(resume, input):
#     test_case = LLMTestCase(
#     input=input, 
#     actual_output=resume
#     )
#     summarization_metric = SummarizationMetric()
#     return evaluate([test_case], [summarization_metric])