import json
def readjson(filePath:str) -> list:
    raw_data = []
    with open(filePath, 'r', encoding='utf-8') as file:
 
        raw_data = json.load(file)
    return raw_data
"""
"is an explanationof", 
"has an explanation",
"is an image of", 
"has an image", 
"is a video of",
"has a video", 
"is an audio of", 
"has an audio", 
"related to". 
"is an exercise of"  
"has an exercise".
"""
def conceptTriples(conceptPath):
    rawdata = readjson(conceptPath)
    textList = []
    imageList = []
    videoList = []
    audioList = []
    knowledgeList = []
    for item in rawdata:
        #text
        textList.append((item['concept'],"has an explanation",item['explanation']))
        textList.append((item['explanation'],"is an explanationof" ,item['concept']))
        #image
        if "none" not in item['png']:
            for image in item['png']:
                imageList.append((item['concept'],"has an image",image))
                imageList.append((image,"is an image of",item['concept']))
        #video
        if "none" != item['videoUrl']:
            videoList.append((item['concept'],"has a video",item['videoUrl']))
            videoList.append((item['videoUrl'],"is a video of",item['concept']))
        #audio
        audioList.append((item['concept'],"has an audio",item['audio']))
        audioList.append((item['audio'],"is an audio of",item['concept']))
        #knowledge
        knowledgeList.append((item['concept'],"related to",item['knowledgePointID']))
        knowledgeList.append((item['knowledgePointID'],"related to",item['concept'])) 
        
 
    allTriples = textList + imageList + videoList + audioList + knowledgeList
    return allTriples
def knowledgeTriples(knowledgePath):
    rawdata = readjson(knowledgePath)
 
    exerciseList = []
    knowledgeList = []
    for item in rawdata:
       
        if "none" != item['ExerciseURL']:
            exerciseList.append((item['KnowledgePointID'],"has an exercise",item['ExerciseURL']))
            exerciseList.append((item['ExerciseURL'],"is an exercise of"  ,item['KnowledgePointID']))
       
        if item['RelatedKnowledgePointID'] != []:
            for i in rawdata:
                if i['KnowledgePointID'] == item['RelatedKnowledgePointID']:
                    knowledgeList.append((item['KnowledgePoint'],"related to",i['KnowledgePoint']))

    return exerciseList + knowledgeList
    
          
allTriples1 = conceptTriples() 
allTriples2 = knowledgeTriples()   
print("The number of triples  is: ", len(allTriples1+allTriples2))
with open(r"", 'w', encoding='utf-8') as merged_file:
        json.dump(allTriples1+allTriples2, merged_file, ensure_ascii=False, indent=4)