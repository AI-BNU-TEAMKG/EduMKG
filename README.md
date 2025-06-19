### EduMKG: A Multimodal Knowledge Graph for Education with Text, Video, Image and Audio
EduMKG is a multimodal educational knowledge graph dataset that covers natural sciences (biology, physics, and chemistry) in middle and high school education. It includes multimodal concepts covering text, images, videos, and audio, as well as knowledge points and exercises extracted from curriculum standards and MOOCs. EduMKG comprises 34,630 multimodal concepts and 403,400 triples, making it a vital resource for research in multimodal educational applications.

This repository contains the models and datasets described in our paper, `EduMKG: A Multimodal Knowledge Graph for Education with Text,  Image, Video and Audio`

#### 🎯🎯🎯Recent Update for EduMKG 
**We sincerely thank all the reviewers for their valuable guidance on our work**
1. We have open-sourced the RDF data of EduMKG on Zenodo at xxx.
2. We have open-sourced an automation script for converting JSON  to RDF format in the RDF folder of this code repository.
3. We have provided a detailed explanation of the ontology design and data definition of the knowledge graph.
4. We have released a SPARQL endpoint and provided basic usage examples.

##### EduMKG ontology

##### Data Definition
| Data Type            | Definition                                                                                 | Mathematical Formalization                                |
|----------------------|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Knowledge Point      | The core facts, skills, or principles of a specific discipline, potentially linked to other concepts and Knowledge Points. | KP = \{ id, name, associated\_concepts, associated\_knowledge_points \}        |
| Multimodal Concept   | A concept represented by data from four distinct modalities.                              | MC = \{ id, name, T, I, V, A, associated\_knowledge\_points \}|
| Subject              | A high-level category that groups related knowledge points.                               | S = \{ id, name, associated\_knowledge\_points \}  |
| Explanation          | A textual description providing detail or clarification for concepts.                    |  T = \{ id, text\_content, associated\_concepts\}                         |
| Image                | A visual representation in PNG format associated with concepts.                         |  I = \{ id, name, associated\_concepts \}                            |
| Video                | A video representation with a URL associated with concepts.                        |  V = \{ id, URL, associated\_concepts \}                                   |
| Audio                | An audio explanation in MP3 format associated with concepts.                            |  A = \{ id, name, associated\_concepts \}                           |
| Exercise             | A task or problem with a URL associated with knowledge points.        | Ex = \{ id, url, associated\_knowledge\_point \}    |
##### SPARQL Endpoint Url and Usage Instructions
We have open-sourced the RDF data of EduMKG on Zenodo and provided an automation script for converting JSON to RDF format in the RDF folder of this code repository. You can execute the script by following the steps below:

1. Install `rdflib`  
```shell  
pip install rdflib  
```  

2. Configure the paths for the input JSON file and the output file, then run `rdf.py`:  
```python  
python rdf.py  
```sparql
3. Accessing the SPARQL Endpoint and Performing Queries: We provide an example for reference.  
* Access the \url{Apache Jena Fuseki UI}.  
* Enter the username and password: `user`, `userPassword`.  
* Example usage:  
   ```
   # Query the concept of “细胞”corresponding to its explanation
   PREFIX ex: <http://v1.edumkg.org/>
SELECT ?explanation
WHERE {
  ?concept a ex:Concept .
  ?concept ex:hasAnExplanation ?explanation .
  FILTER(CONTAINS(STR(?concept), ENCODE_FOR_URI("细胞")))
}
```



#### Dataset and Models
* `Dataset`: All information about EduMKG is at https://zenodo.org/records/15386565, including extracted raw data from MOOCs and generated EduMKG.
* `Code`: All the code referenced in the paper is available in this repository. Additionally, we have released a Python library for automatically constructing multimodal educational knowledge graphs at [EduMKG-Python-Library](https://github.com/AI-BNU-TEAMKG/EduMKG-Python-Library)
#### Folder Structure
* `Dataprocess`: This folder contains scripts and utilities for data preprocessing. It includes functionalities for cleaning, transforming, and preparing raw datasets for further analysis.
* `ExtractMultimodalConcepts`: This folder contains code for extracting concepts.
* `EduMKGConstruction`: This folder contains code for building a knowledge graph based on multimodal educational data.
* `MultimodalAlignment`: This folder provides code for aligning multimodal data across different modalities.

#### Prerequisites
* Python >= 3.7
* Required dependencies as listed in `requirements.txt`

Contact
If you have any questions or feedback about the EduMKG dataset, please feel free to contact us at ethanlu[at]mail.bnu.edu.cn

Thank you for being so interested in EduMKG!
