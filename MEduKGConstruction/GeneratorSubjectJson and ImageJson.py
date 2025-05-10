import json
from collections import OrderedDict
import time
"""
1.add id
"""


file_path = r""


try:
    with open(file_path, "r", encoding="utf-8") as file:  
        data = json.load(file)  
except FileNotFoundError:
    print(f" {file_path} ")
    exit(1)
except json.JSONDecodeError:
    print(f" {file_path} ！")
    exit(1)
except UnicodeDecodeError as e:
    print(f" {file_path} {e}")
    exit(1)


processed_data = []


for i, item in enumerate(data, start=1):
    ordered_item = OrderedDict()
    ordered_item["id"] = i-1  
    for key, value in item.items():
        ordered_item[key] = value 
    processed_data.append(ordered_item)


try:
    with open(r"", "w", encoding="utf-8") as file:  
        json.dump(processed_data, file, ensure_ascii=False, indent=4)
    print(f" {file_path} ")
except Exception as e:
    print(f"入文件 {file_path} {e}")
    exit(1)


print("")
print(json.dumps(processed_data, ensure_ascii=False, indent=4))





"""
2. add image
"""
def read_file1(file1_path):
    file1_data = {}
    with open(file1_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) > 1:
                png_name = parts[0]
                ids = parts[1:]
                for id_ in ids:
                    if id_ not in file1_data:
                        file1_data[id_] = []  
                    file1_data[id_].append(png_name)  
    return file1_data


def read_file2(file2_path):
    with open(file2_path, "r", encoding="utf-8") as file:  
        data = json.load(file) 
    return data


def update_file2_with_png(file1_data, file2_data):
    cnt = 0
    cnta = 0
    for entry in file2_data:
        concept_id = str(entry.get("id")) 
        if concept_id in file1_data:
            entry["png"] = file1_data[concept_id]  
            cnta += 1
        else:
            entry["png"] = ["none"]  
            cnt += 1
    return file2_data, cnt, cnta


def main():
    file1_path =
    file2_path = 
    output_file2_path = 


    file1_data = read_file1(file1_path)
    file2_data = read_file2(file2_path)


    updated_file2, cnt, cnta = update_file2_with_png(file1_data, file2_data)


    with open(output_file2_path, "w", encoding="utf-8") as output_file:
        json.dump(updated_file2, output_file, indent=4, ensure_ascii=False)

    print(f"{cnta}  {cnt + cnta}")


if __name__ == "__main__":
    main()


"""
3.add audio
"""
import os
import json


json_file_path =
audio_folder_path = 


valid_extensions = ['.mp3', '.wav']


with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)


for item in data:
    concept = item['concept']
    file_id = item['id']


    for file_name in os.listdir(audio_folder_path):
  
        name, ext = os.path.splitext(file_name)

  
        if ext not in valid_extensions:
            continue

    
        if name == concept:
          
            new_file_name = f"{file_id}_{file_name}"

        
            old_file_path = os.path.join(audio_folder_path, file_name)
            new_file_path = os.path.join(audio_folder_path, new_file_name)

          
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {old_file_path} -> {new_file_path}")

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
for item in data:
    item["audio"] = item["id"]
    
json_file_path = 
with open(json_file_path, "w", encoding="utf-8") as output_file:
    json.dump(data, output_file, indent=4, ensure_ascii=False)








"""
4.generate image json
"""
import json

def convert_to_json(file_path):

    result = {}


    with open(file_path, 'r') as file:
        for line in file:

            parts = line.strip().split()
 
            key = parts[0]
     
            values = list(map(int, parts[1:]))
      
            result[key] = values

    return result


file_path = 

json_output = convert_to_json(file_path)


json_file_path =
with open(json_file_path, "w", encoding="utf-8") as output_file:
    json.dump(json_output, output_file, indent=4, ensure_ascii=False)
