import json
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS
from urllib.parse import quote


def convert_json_to_rdf_xml(json_file_path, rdf_file_path):
    """
    
    Args:
        json_file_path (str): 
        rdf_file_path (str): 
    """
    
    g = Graph()
    EX = Namespace("http://v1.edumkg.org/")
    g.bind("ex", EX)  
    g.bind("rdf", RDF) 
    g.bind("rdfs", RDFS) 


    Concept = EX.Concept
    KnowledgePoint = EX.KnowledgePoint
    Image = EX.Image
    Video = EX.Video
    Audio = EX.Audio
    Exercise = EX.Exercise

    class_labels = {
        Concept: "conceptType",
        KnowledgePoint: "knowledgepointType",
        Image: "imageType",
        Video: "videoType",
        Audio: "audioType",
        Exercise: "exerciseType"
    }
    for cls, label in class_labels.items():
        g.add((cls, RDFS.label, Literal(label, lang="zh-cn")))


    def to_camel_case(text: str) -> str:
        text = text.replace('_', ' ') 
        words = text.strip().split()
        if not words:
            return ""
        return words[0].lower() + "".join(word.capitalize() for word in words[1:])

    try:

        with open(json_file_path, 'r', encoding='utf-8') as f:
            triples = json.load(f)

        nodes_with_type = set() 

 
        for s_text, p_text, o_text in triples:
       
            s_text, p_text, o_text = str(s_text).strip(), str(p_text).strip(), str(o_text).strip()
            
    
            subject_uri = EX[quote(s_text)]
            predicate_uri = EX[to_camel_case(p_text)]

       
            if p_text == "has an explanation":
                obj = Literal(o_text, lang="zh-cn")
            else:
                obj = EX[quote(o_text)]
            

            g.add((subject_uri, predicate_uri, obj))

    
            type_map = {
                "is an explanationof": (KnowledgePoint, Concept),
                "explanation_of": (KnowledgePoint, Concept),
                "related to": (Concept, Concept),
                "image_of": (Image, Concept),
                "video_of": (Video, Concept),
                "audio_of": (Audio, Concept),
                "exercise_of": (Exercise, Concept)
            }

            object_is_uri = isinstance(obj, URIRef) 
            if p_text == "has an explanation":
                if subject_uri not in nodes_with_type:
                    g.add((subject_uri, RDF.type, Concept))
                    nodes_with_type.add(subject_uri)
            elif p_text in type_map:
                s_type, o_type = type_map[p_text]
                if subject_uri not in nodes_with_type:
                    g.add((subject_uri, RDF.type, s_type))
                    nodes_with_type.add(subject_uri)
                if object_is_uri and obj not in nodes_with_type:
                    g.add((obj, RDF.type, o_type))
                    nodes_with_type.add(obj)


        g.serialize(destination=rdf_file_path, format='pretty-xml', encoding='utf-8')
        print(f" '{json_file_path}' '{rdf_file_path}'。")

    except FileNotFoundError:
        print(f" '{json_file_path}'。")
    except json.JSONDecodeError:
        print(f"'{json_file_path}'")
    except Exception as e:
        print(f" {e}")



if __name__ == '__main__':
    input_json_file = 
    output_rdf_file = 

    convert_json_to_rdf_xml(input_json_file, output_rdf_file)
