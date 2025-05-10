import requests
from urllib.parse import urljoin
import re

def get_english_terms(chinese_concept: str) -> list:
    url = f"https://api.conceptnet.io/c/zh/{chinese_concept}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f": {e}")
        return []
    
    terms = set()
    for edge in data.get("edges", []):
  
        for node in [edge.get("start"), edge.get("end")]:
            if not node:
                continue
            if node.get("language") == "en":
                term = node.get("term", "")
           
                if term.startswith("/c/en/"):
                    parts = term.split('/')
                  
                    if len(parts) >= 4:
                        base_term = '/'.join(parts[:4])
                        terms.add(base_term)
    return list(terms)

def fetch_surface_texts(term: str) -> list:

    api_url = urljoin("https://api.conceptnet.io", term)
    try:
        response = requests.get(api_url, params={"limit": 100}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f": {api_url} | : {e}")
        return []
    
    texts = set()
    for edge in data.get("edges", []):
        surface_text = edge.get("surfaceText")
        if surface_text:
        
            clean_text = surface_text.replace("[[", "").replace("]]", "").strip()
            texts.add(clean_text)
    return sorted(texts) 

def get_surface_texts(chinese_concept: str) -> list:
    print(f": {chinese_concept}")
    
   
    en_terms = get_english_terms(chinese_concept)
    if not en_terms:
        print("no term")
        return None,None
    
 
    results = {}
    for term in en_terms:
        texts = fetch_surface_texts(term)
        results[term] = texts
    
   
    print("\nSurfaceText:")
    result_text = []
    results_term = " "
    for term, texts in results.items():
        print(f"\nTerm: {term}")
        results_term = term.split('/')[-1].replace('_', ' ')
        for idx, text in enumerate(texts, 1):
            print(f"  {idx}. {text}")
            result_text.append(text)
    return result_text,results_term


def extract_cell_nouns(lines: list, results_term: str) -> list:
    nouns = set()
    results_term = results_term.lower()
    patterns = [
              # your rules
    ]
    print("====================================")
    for line in lines:

        line_content = re.sub(r'^\d+\.\s*', '', line.strip())

        line_lower = line_content.lower()
        
        for pattern, target in patterns:
            match = re.match(pattern, line_lower, re.IGNORECASE)
            if match:
             
                if target == 'direct':
                    word = match.group(1)
                elif target == 'x':
                    word = match.group(1)
                elif target == 'y':
                    word = match.group(1)
                else:
                    continue
                
             
                word = re.sub(r'^(a|an|the)\s+', '', word, flags=re.IGNORECASE)
             
                original_word = match.group(1) if target != 'direct' else match.group(1).upper()
                nouns.add(original_word.strip())
                break  
    
    return sorted(nouns)


if __name__ == "__main__":
    result_text,results_term =  get_surface_texts("")
    related_nouns = extract_cell_nouns(result_text,results_term)
    print(fr"{results_term} ：")
    candidate_list = []
    for noun in sorted(related_nouns):
        print(f"- {noun.capitalize()}")
        candidate_list.append(noun.capitalize())
    print(len(candidate_list))
    

            
