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
import base64


concept = []
#count_global = 3890
def imageAnalysis(image_path: str, subject: str, concepts: list ,model="gpt-4o") -> str:
    prompt = f"""
        You are an AI  {subject} image analyst. Follow this strict protocol:
        1. Candidate Verification:
           Within the {subject} concepts {concepts},
           identify and extract the concepts that appear in the image or are highly related to it. 
           Use these extracted concepts to form the C4 .
        2. Multilevel Analysis:
        a) OCR Extraction: Capture ALL {subject} pure concept  in  → C1
        b) Regional Analysis: Identify specific  {subject} components → C2
        c) Holistic Analysis: Derive tissue/system-level {subject} concepts → C3
        3. Deduplication Protocol:
        Priority: C4 > C3 > C2 > C1
        - Remove duplicates ONLY for identical terms
        - Preserve hierarchical terms (e.g., keep both "" and "")
        4. Output Decision:
        - If any valid terms remain: List ALL in bullet format
        - If completely empty: Output "none"
        Mandatory Format:
        - concept1
        - concept2
        ...

        OR
        "none"
        Absolute constraints:
        1. No term suppression except exact duplicates
        2. No explanations, categories, or formatting variations.
    """
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")   
    url = ""
    payload = json.dumps({
    "model": model,
    "messages": [
        {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                ],
            }
    ]
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': '',
        'Content-Type': 'application/json'
    }
    while True:
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        except:
            print("error")
            print(response)
            time.sleep(65)
            continue

def mainImages(file_path: str, jsonFile:str, subject: str) -> None:
 
    imageC = {}
    with open(f"imageConceptIndex_{subject}", "a+", encoding="utf-8") as files:
        files.seek(0)  
        content = files.read()
        #cnt = 4492
        cnt  = 0
        
        # obtain all txt
        txt_files = glob.glob(os.path.join(file_path, '**', '*Intergrationner'), recursive=True)
        for txt_file in txt_files:
            # print("*"*10)
            # print(txt_file)
            # print("*"*10)
            concepts_list = []
            data = {}
            with open(txt_file, 'r', encoding='utf-8') as file:
                for line in file:
                    match = re.match(r'(\d{2}:\d{2}-\d{2}:\d{2})\s+(.+)', line.strip())
                    if match:
                        time_range, concepts = match.groups()
                        for con in concepts.split():
                            if con not in concepts_list:
                                concepts_list.append(con) 

            #==========================================================      
            folder_path = os.path.dirname(txt_file)
            allfiles = os.listdir(folder_path)
            png_files = []
            for ele in allfiles:
                if "bmp" in ele:
                    continue
                if "png" in ele or "0-00000" in ele.strip('.'):
                    png_files.append(folder_path + "/" + ele)
            #png_files = glob.glob(os.path.join(folder_path,"*png"))

            add_concepts = []
            for png in png_files:
                #if cnt <= 133:
                   # cnt += 1
                  #  continue
                print(png,cnt)
                imageC[str(cnt)+".png"] = []
                time.sleep(2)
                result1  = imageAnalysis(png, subject, concepts_list, model="gpt-4o-2024-11-20")
                time.sleep(3)
                result2 = imageAnalysis(png, subject, concepts_list, model="gpt-4o-2024-11-20")
                time.sleep(3)
                result3 = imageAnalysis(png, subject, concepts_list, model="gpt-4o-2024-11-20")
                result1 = re.findall(r"-\s*(\w+)", result1)
                result2 = re.findall(r"-\s*(\w+)", result2)
                result3 = re.findall(r"-\s*(\w+)", result3)
                result = set(result1) | set(result2) | set(result3)
                print("*"*10)
                print(f" png {png}   ok  cnt{cnt}\n")
                print("*"*10)
                
                if result == "none":     
                    continue   
                else:
                    #result =  re.findall(r"-\s*(\w+)", result)
                    print(result)
                    for r in result:
                        try:
                            index = concept.index(r)
                            imageC[str(cnt)+".png"].append(index)
                        except:
                            concept.append(r)
                            add_concepts.append(r)
                            imageC[str(cnt)+".png"].append(len(concept)-1)
                directory = os.path.dirname(png)
                new_path = os.path.join(directory, str(cnt)+".png")
                os.rename(png, new_path)
                files.write(f"{str(cnt)}.png ")
                for i in imageC[str(cnt)+".png"]:
                    files.write(str(i)+" ")
                files.write("\n")
                
                
                cnt += 1

                                           
def readConcepts(conceptPath: str) -> None:

    global concept
    with open(conceptPath, "r", encoding="utf-8") as f:
        
        existing_data = json.load(f)
    for item in existing_data:
        concept.append(item['concept'])
    f.close()
    
if __name__ == "__main__":
    subject = ""
    fileList = [r""]
    jsonFile = r""
    
    readConcepts(jsonFile)
    
    for ele in fileList:
        mainImages(ele, jsonFile, subject)
