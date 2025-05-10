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
allEntity = set()
finalEntity = set()

def process_directory(directory_path: str, models: list, subject: str, k: int) -> None:
    # obtain all txt
    txt_files = glob.glob(os.path.join(directory_path, '**', '*.txt'), recursive=True)
    for txt_file in txt_files:
        ner_file_path = txt_file.replace('.txt', '_Extractionner')
        # skip processed txt
        if os.path.exists(ner_file_path):
            continue
        # extract concepts
 
        candidate = extractConcepts(txt_file, models, subject,allEntity,k) 
        
    # expand concepts and link explanations
    #results = expandExplanations(subject)
    
    # with open(f"{subject}", 'w', encoding='utf-8') as f: 
    #     for item in results:
    #         f.write(item[0])
    #         f.write("\t")
    #         f.write(item[1])
    #         f.write("\n")
    # f.close()
                  
def extractConcepts(filePtah: str,models: list, subject: str, allEntity: set, k=3) -> list:

    
    """candidate format
    results.append([timestamp,candidate_set,sc_score,prompt])
    timestamp1, entities_set1, sc_score, prompt, max
    timestamp2, entities_set2, sc_score, prompt, max
    timestamp3, entities_set3, sc_score, prompt, max
    ...
    """

    # Extraction
    candidate = Extraction(filePtah, models, subject, allEntity, k)

    # Validation models  default k=5
    candidate = Validation(candidate, models, subject, k,filePtah)
    # Intergration
    candidate = Intergration(candidate,k,filePtah)

    return candidate
            
def Extraction(filePtah: str, models: str, subject: str, allEntity: set, k: int) -> Tuple[dict, set]:
    ner_file_path = filePtah.replace('.txt', '_Extractionner')
    with open(filePtah, 'r', encoding='utf-8') as file:
            print("*************************************")
            print(filePtah)
            print("*************************************")
            # save all entity in all time
            entity_set = set()
            # save entity and time in special time 
            entity_time_set = dict()
            prompt = f"""
            $
            Silently analyze the text to:
            a) Identify all nouns/noun phrases using syntactic tagging
            b) Filter these to retain only concepts related to {subject}
            c) STRICTLY OUTPUT ONLY the final {subject} concepts: In Simplified Chinese 
            As a single list using this exact format: -xxx\n-xxx\n-xxx
            No headers/explanations/other text
            Never reveal non-subject nouns or intermediate analysis.
            $
            """
            for line in file:
                try: 
                    timestamp, content = line.strip('"').split('": "', 1)
                    entity = ner("deepseek-v3", content + prompt)
                    entity =  re.findall(r"-\s*(\w+)", entity)
                    # save entity in this time  
                    entity_time = set()
                    # for
                    for item in entity:
                        if item not in allEntity:
                            allEntity.add(item)
                            entity_time.add(item)
                            entity_set.add(item)
                    entity_time_set[timestamp] = entity_time         
                except:
                    continue
                print("=====================================")  
                print(f"timestamp: {timestamp} Entities: {entity_set} model: deepseek-v3 ")
                print("=====================================")         

    
    results = []
    for timestamp, candidate_set in entity_time_set.items():
        sc_score = [1]*len(candidate_set)
        max = [1]*len(candidate_set)
        prompt = "hello,"
        results.append([timestamp,candidate_set,sc_score,prompt,max])
    print(results)
        
        
    # TODO write the results to file
    if not os.path.exists(ner_file_path):
        with open(ner_file_path, 'w', encoding='utf-8') as ner_file:
            for item in results:
                ner_file.write(f"{item[0]}")
                ner_file.write('\n')
                for entity in item[1]:
                    ner_file.write(f"{entity} ")
                ner_file.write('\n')
                for score in item[2]:
                    ner_file.write(f"{score} ")
                ner_file.write('\n')
                ner_file.write(f"{prompt}")
                ner_file.write('\n')
                for max in item[4]:
                    ner_file.write(f"{max} ")
                ner_file.write('\n')
                ner_file.write('\n')
                
                
        ner_file.close()
        
            
    else:
        with open(ner_file_path, 'a', encoding='utf-8') as ner_file:
            for item in results:
                ner_file.write(f"{item[0]}")
                ner_file.write('\n')
                for entity in item[1]:
                    ner_file.write(f"{entity} ")
                ner_file.write('\n')
                for score in item[2]:
                    ner_file.write(f"{score} ")
                ner_file.write('\n')
                ner_file.write(f"{prompt}")
                ner_file.write('\n')
                for max in item[4]:
                    ner_file.write(f"{max} ")
                ner_file.write('\n')
                ner_file.write('\n')
                
        ner_file.close()
    return results

def Validation(candidate: list, models: str, subject: str, k: int, filePtah: str) -> list:
    """candidate format
    results.append([timestamp,candidate_set,sc_score,prompt])
    timestamp1, entities_set1, sc_score, prompt, max
    timestamp2, entities_set2, sc_score, prompt, max
    timestamp3, entities_set3, sc_score, prompt, max
    ...
    """
    # k = iter
    # SELF-REFINE
    candidate = SELF_REFINE(candidate,subject,models,k,filePtah)
    return candidate

def SELF_REFINE(candidate: list, subject: str, models: str, k: int, filePtah:  str) -> str: 

    FEED_BACKE_internal_prompt = f"""
    $
    ---
    Analyze the extracted K-12 {subject} concepts to:
    a) NEVER modify or split original terms
    b) Identify terms with cross-disciplinary ambiguity (e.g., terms that hold distinct meanings in other academic fields)
    c) For each ambiguous term, provide a one-sentence clarification of its potential alternative academic meaning
    d) Format output EXACTLY as: "ambiguous term" ："reason"
    e) Output ONLY lines following this format without additional text
    f) Preserve original lexical structure
    
    Example analysis pattern:
    "系统" : "Could refer to computer systems in technology contexts"
    
    $
    """
    

    """candidate format
    results.append([timestamp,candidate_set,sc_score,prompt])
    timestamp1, entities_set1, sc_score, prompt, max
    timestamp2, entities_set2, sc_score, prompt, max
    timestamp3, entities_set3, sc_score, prompt, max
    ...
    """
    results = []

    for timestamp, entities_set, sc_score, prompt, max in candidate:
        if len(entities_set) == 0:
            continue
        candidate_list = list()
        for entity in entities_set:
            candidate_list.append(entity)
        for model in models: 
            sc_max = [0]*len(entities_set)
            prompt = "hello, "
            for i in range(0,k):
                
            # FEED_BACKE
                tmp = str(candidate_list)
                feedback = ner(model, tmp + FEED_BACKE_internal_prompt + prompt)
                
                # RE_FINE
                RE_FINE_internal_prompt = f"""
                $
                Concept Filtering Protocol for K-12 {subject}

                FEEDBACK ANALYSIS
                $
                {feedback}
                $
                (Note: Feedback analysis may contain errors.)
                (Each feedback item clearly indicates terms that are out-of-scope or ambiguous with respect to K-12 {subject}. 
                For example, if feedback for "alcohol" indicates a chemistry context but not {subject}, then "alcohol" must be removed.)
                
                CANDIDATE POOL
                "{candidate_list}"

                1.Perform primary pruning using the FEEDBACK ANALYSIS to remove terms that are not directly relevant to K-12 {subject}.
                2.Secondary filtration: Apply K-12  {subject} standards to ensure that all remaining terms are inherently  {subject} concepts rather than instruments, apparatuses, or tools merely utilized in {subject} experiments.  
                (For example, although microscopes, objective lenses, temporary slides, and illumination components are used in {subject}, they are fundamentally tools from physics or engineering and should be removed.)  
                3. Eliminate redundancies and non-{subject} terms while preserving the original order.

                OUTPUT SPECIFICATIONS
                Strictly output in Markdown list format, with each term on a new line as follows:  
                - concept1  
                - concept2  
                - concept3  
                Maintain the original order of valid entries.  
                Output only the list, with no additional text.

                Filtered Result:  
                $
                    
                """
                print("*"*9)
                print(RE_FINE_internal_prompt)
                entity = ner(model,RE_FINE_internal_prompt)
                entity =  re.findall(r"-\s*(\w+)", entity)
                print(entity,model)
                print("*"*9)
                prompt = prompt + feedback + "\n"
                # SC_SCORE 
                entity = set(entity)
                for index , i in enumerate(entities_set):
                    if i in entity:
                        sc_score[index] += 1
                        sc_max[index] +1

            for index, (i , j) in enumerate(zip(sc_max, max)) :
                if i > j:
                    max[index] = i
                else:
                    max[index] = j

        results.append([timestamp,entities_set,sc_score,prompt,max])
    for item in results:
        print(f"timestamp: {item[0]} Entities: {item[1]}")

    # TODO write the results to file
    ner_file_path = filePtah.replace('.txt', '_Validationner')
    if not os.path.exists(ner_file_path):
        with open(ner_file_path, 'w', encoding='utf-8') as ner_file:
            for item in results:
                ner_file.write(f"{item[0]}")
                ner_file.write('\n')
                for entity in item[1]:
                    ner_file.write(f"{entity} ")
                ner_file.write('\n')
                for score in item[2]:
                    ner_file.write(f"{score} ")
                ner_file.write('\n')
                ner_file.write(f"{item[3]}")
                for max in item[4]:
                    ner_file.write(f"{max} ")
                ner_file.write('\n')
                ner_file.write('\n')
                
        ner_file.close()
        
            
    else:
        with open(ner_file_path, 'a', encoding='utf-8') as ner_file:
            for item in results:
                ner_file.write(f"{item[0]}")
                ner_file.write('\n')
                for entity in item[1]:
                    ner_file.write(f"{entity} ")
                ner_file.write('\n')
                for score in item[2]:
                    ner_file.write(f"{score} ")
                ner_file.write('\n')
                ner_file.write(f"{item[3]}")
                for max in item[4]:
                    ner_file.write(f"{max} ")
                ner_file.write('\n')
                ner_file.write('\n')
        ner_file.close()         
    return results 

def Intergration(candidate: list, k: int, filePtah: str)-> list:
    # SC_score
    """candidate format
    results.append([timestamp,candidate_set,sc_score,prompt])
    timestamp1, entities_set1, sc_score, prompt, max
    timestamp2, entities_set2, sc_score, prompt, max
    timestamp3, entities_set3, sc_score, prompt, max
    ...
    """
    results = []
    for timestamp, entities_set, sc_score, prompt, max in candidate:
        final_entity = set()
        for index, i in enumerate(entities_set):
            # condition 1
            SC_ScoreG = (1 / k * k)  * sc_score[index]
    
            if SC_ScoreG > 0.6:
                final_entity.add(i)
                
            # condition 2
            if max[index] == k:
                final_entity.add(i)
        results.append([timestamp,final_entity])
        print(f"timestamp: {timestamp} Entities: {final_entity}")
    # TODO write the results to file
    ner_file_path = filePtah.replace('.txt', '_Intergrationner')
    if not os.path.exists(ner_file_path):
        with open(ner_file_path, 'w', encoding='utf-8') as ner_file:
            for item in results:
                ner_file.write(f"{item[0]}")
                ner_file.write('\n')
                for entity in item[1]:
                    ner_file.write(f"{entity} ")
                    finalEntity.add(entity)
                    
                ner_file.write('\n')
                ner_file.write('\n')
                
        ner_file.close()
    return results
      
def expandExplanations(subject: str) -> list:
    entity_explanation = []

    conceptExpand(subject)
    

    for item in finalEntity:
        expandExplanations =  get_wikipedia_summary(item)
        if expandExplanations == "not found":
            propmt = f"""
            $
            You will be provided with a {subject} discipline concept. Generate one concise Chinese sentence describing it, 
            strictly within 20 words. Use simple language, prioritize accuracy, and avoid technical jargon unless critical. 
            Output only the final sentence without explanations, punctuation, or markdown. The concept is 
            $  
            """      
            explanation = ner("deepseek-v3",propmt+str(item))
            entity_explanation.append([item,explanation])  
             
        else:
            propmt = f"""
            "Given a concept from the {subject} discipline, with its Wikipedia explanation provided as '{expandExplanations}', 
            generate a concise one-sentence Chinese description (≤20 words) strictly based on the Wikipedia content. 
            Output only the generated description without explanations or markdown."
            """    
            explanation = ner("deepseek-v3",propmt+str(item))
            entity_explanation.append([item,explanation])  
            
  
  
    return entity_explanation

def conceptExpand(subject: str)-> list:

    prompt = f"""
    Silently analyze the text to:
                a) Filter these to keep ONLY K-12 pure {subject} concepts 
                b) STRICTLY OUTPUT ONLY the final pure {subject} concepts: In Simplified Chinese 
                As a single list using this exact format: -xxx\n-xxx\n-xxx
                No headers/explanations/other text
                Never reveal non-subject nouns or intermediate analysis.   
    """
    result = []
    
    for item in finalEntity:
        result_text,results_term = get_surface_texts(item)
        if result_text == None:
            continue
        related_nouns = extract_cell_nouns(result_text,results_term)
        if len(related_nouns) == 0:
            continue
        add_list = []
        for noun in sorted(related_nouns):
            print(f"- {noun.capitalize()}")
            add_list.append(noun.capitalize())
            
        add_list = str(add_list)
        entity = ner("deepseek-v3",add_list+prompt)
        entity =  re.findall(r"-\s*(\w+)", entity)
        for i in entity:
            if i not in allEntity and i not in finalEntity:
                result.append(i)
    for item in result:
        finalEntity.add(item)
    return result
    
def ner(model:str,content:str) -> str:
    url = 
    payload = json.dumps({
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": content
        }
    ]
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 
        'Content-Type': 'application/json'
    }

    time.sleep(2)
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    print("=============================================")
    print(content)
    print(response)
    print("=============================================")
    response_json = response.json()
    while True:
        try:
            return response_json["choices"][0]["message"]["content"]
        except:
            print(f"retry   {model}")
            time.sleep(70)
            a = ner(model,content)
            if a :
                return a
              
    
def main(filePathList: str, subject: str, models: list) -> None:
    for path_to_your_directorys in filePathList:
        process_directory(path_to_your_directorys, models, subject, k=5)    
        
if __name__ == "__main__":

    models = ["gpt-4o-mini","deepseek-v3","gemini-1.5-flash"]
    
    filePathList =  [

    ]
    subject = "Physics"
    main(filePathList, subject, models)

    