import numpy as np
import itertools
from typing import List
import regex as re

def chop_and_chunk(text, max_seq_length):
    """
    Chop and chunk a text into smaller pieces of text. 
    
    Args:
    text: string, list of strings, or array of strings 
    max_seq_length: maximum length of the text
    """
    if isinstance(text, str):
        text = [text]

    # If text is already split into chunks by newlines, simply return it 
    if all('\n' in t for t in text):
        return text 

    chunks = []
    for t in text: 
        # Split by newlines 
        parts = re.split('\n+', t)  

        for p in parts:
            tokens = p.split()
            chunk = ''
            count = 0
            for t in tokens:
                if count + len(t) < max_seq_length:
                    count += len(t) 
                    chunk += t + ' '
                else:
                    chunks.append(chunk.strip())
                    count = 0
                    chunk = ''
            if chunk != '':
                chunks.append(chunk.strip())
    return chunks
        
def split_text(text, max_seq_length):
    def split_paragraph(paragraph):
        words = paragraph.split()
        return [' '.join(words[i:i+max_seq_length]) for i in range(0, len(words), max_seq_length)]

    chunks = [chunk for t in text for paragraph in re.split('\n+', t) for chunk in split_paragraph(paragraph)]
    return chunks
    
def cos_sim(a, b):
    sims = a @ b.T
    sims /= np.linalg.norm(a) * np.linalg.norm(b, axis=1) 
    return sims
