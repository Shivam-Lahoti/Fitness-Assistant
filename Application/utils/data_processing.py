import re
import pandas as pd

def clean_text(text):
    """
    Cleans text data by removing unwanted characters and formatting issues.
    """
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters
    return text.strip()

def preprocess_csv(file_path, text_column):
    """
    Preprocesses a CSV file containing text data.
    
    Args:
        file_path (str): Path to the CSV file.
        text_column (str): Column containing text data to be cleaned.
    
    Returns:
        List[str]: Cleaned text data.
    """
    df = pd.read_csv(file_path)
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in the dataset.")
    df[text_column] = df[text_column].apply(clean_text)
    return df[text_column].tolist()

def save_cleaned_data(data, output_path):
    """
    Saves cleaned data to a text file.
    
    Args:
        data (List[str]): List of cleaned text data.
        output_path (str): File path to save the cleaned data.
    """
    with open(output_path, 'w') as f:
        for line in data:
            f.write(f"{line}\n")
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    # Example usage
    cleaned_text = preprocess_csv("data/fitness_data.csv", text_column="content")
    save_cleaned_data(cleaned_text, "data/cleaned_fitness_data.txt")
