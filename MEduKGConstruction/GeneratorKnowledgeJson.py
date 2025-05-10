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
        # 使用 json.load() 解析 JSON 数据
        raw_data = json.load(file)
    return raw_data
stard = readjson(r'F:\2.实验\3.Datasets\1.国家中小学智慧平台数据集\0.smartEdu\Course\json\biology\knowledgeBiology.json')
charp = readjson(r'F:\2.实验\3.Datasets\1.国家中小学智慧平台数据集\0.smartEdu\Course\json\biology\biologyURL.json')

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
    
with open(r"F:\2.实验\3.Datasets\1.国家中小学智慧平台数据集\0.smartEdu\Course\json\biology\biologyKnowledge.json", 'w', encoding='utf-8') as merged_file:
    json.dump(result, merged_file, ensure_ascii=False, indent=4)

