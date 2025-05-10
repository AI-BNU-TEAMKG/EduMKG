"""
KnowledgePoint ID
KnowledgePoint
Related KnowledgePoint ID
Exercise ID
"""
import json
def readjson(filePath:str) -> list:
    raw_data = []
    with open(filePath, 'r', encoding='utf-8') as file:

        raw_data = json.load(file)
    return raw_data
stard = readjson(r')
charp = readjson(r'')

start = 0
result = []
for key, value in charp.items():
    new = {}
    new['KnowledgePointID'] = start
    new['KnowledgePoint'] = key
    new['RelatedKnowledgePointID'] = []
    new['ExerciseURL'] = value
    result.append(new)
    start += 1
    
for key, value in stard.items():
    new = {}
    new['KnowledgePointID'] = start
    new['KnowledgePoint'] = key
    new['RelatedKnowledgePointID'] = "none"
    for item in result:
        if item['KnowledgePoint'] == value:
            item['RelatedKnowledgePointID'] = start
            new['RelatedKnowledgePointID'] = item['KnowledgePointID']
            break
    new['ExerciseURL'] = "none"
    result.append(new)
    start += 1
    
with open(r"n", 'w', encoding='utf-8') as merged_file:
    json.dump(result, merged_file, ensure_ascii=False, indent=4)

