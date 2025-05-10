# -*- coding: utf-8 -*-
import requests
import json
import os
import glob
import time
from typing import Tuple
import os
from openai import OpenAI
import re
from ConceptNet import *
from wikipediaapi_model import *
from NER import *
concepts = {}
result = []
def process_directory(directory_path: str, models: list, subject: str, k: int) -> None:
    # obtain all txt
    txt_files = glob.glob(os.path.join(directory_path, '**', '*_Intergrationner'), recursive=True)
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file:
     
                line = line.strip()
             
                if line:
                
                    time_range, concept = line.split(maxsplit=1)
                   
                    concepts[concept] = time_range  
                    
    for key,value in concepts.items():
       result.append([value,key])
    print(result)
    return result

def expandExplanations(subject: str,file_path_finalentity: str) -> list:
    entity_explanation = []
    with open(file_path_finalentity, 'r', encoding='utf-8') as file:
      
        data = json.load(file)

    for i in data:
        if i not in concepts:
            result.append([i,"none"])
    
 
    for index,item in enumerate(result):
        print(f"*****************{len(result)}************{index}****个*****")
        concept = item[1]
        kk =  get_wikipedia_summary(concept)
        if kk == "not found" or kk == "error" :
            propmt = f"""
            $
            You will be provided with a {subject} discipline concept. Generate one concise Chinese sentence describing it, 
            strictly within 20 words. Use simple language, prioritize accuracy, and avoid technical jargon unless critical. 
            Output only the final sentence without explanations, punctuation, or markdown. The concept is {concept}
            $  
            """      
            time.sleep(2)
            explanation = ner("",propmt)
            print(explanation)
            entity_explanation.append([item[0],concept,explanation])  
            print(entity_explanation)
             
        else:
            propmt = f"""
            "Given a concept {concept} from the {subject} discipline, with its Wikipedia explanation provided as '{kk}', 
            generate a concise one-sentence Chinese description (≤20 words) strictly based on the Wikipedia content. 
            Output only the generated description without explanations or markdown."
            """    
            explanation = ner("",propmt)
            print(explanation)
            entity_explanation.append([item[0],concept,explanation])  
            
            
    wr = []
    for item in entity_explanation:
        if item[1] != "none":
            data_dict = {
                "time": item[0],         
                "concept": item[1],       
                "explanation": item[2]    
            }
        else:
            data_dict = {
                "time": item[1],          
                "concept": item[0],       
                "explanation": item[2]    
            }           
        wr.append(data_dict)
    with open("", "w", encoding="utf-8") as f:
        json.dump(wr, f, ensure_ascii=False, indent=4)

    print(" ")      
        
    return entity_explanation

process_directory(
    "", "a", 'a', -1)
entity_explanation = expandExplanations("",r"")