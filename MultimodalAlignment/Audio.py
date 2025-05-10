from Speechgenerator import *
import json
import time
import base64
def main(file_path_finalentity:str,filePath:str) -> None:
    with open(file_path_finalentity, 'r', encoding='utf-8') as file:

        data1 = json.load(file) # type(data1) = list
        for index,i in enumerate(data1):
            concept = i["concept"]
            explanation = i["explanation"]
            while True:
                try:
                    if speechGenerator(explanation, concept, filePath):
                        print(f"*****************{len(data1)}************{index}*********")
                        print("ok")
                    else:
                        print(f"*****************{len(data1)}************{index}*********")
                        print("")
                    break
                except:
                    print("fail...")
                    time.sleep(61)
if __name__ == "__main__":
    file_path_finalentity = r""
    filePath = r""
    main(file_path_finalentity,filePath)