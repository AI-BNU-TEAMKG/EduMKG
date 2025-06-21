### EduMKG: A Multimodal Knowledge Graph for Education with Text, Video, Image and Audio
EduMKG is a multimodal educational knowledge graph dataset that covers natural sciences (biology, physics, and chemistry) in middle and high school education. It includes multimodal concepts covering text, images, videos, and audio, as well as knowledge points and exercises extracted from curriculum standards and MOOCs. EduMKG comprises 34,630 multimodal concepts and 403,400 triples, making it a vital resource for research in multimodal educational applications.

This repository contains the models and datasets described in our paper, `EduMKG: A Multimodal Knowledge Graph for Education with Text, Image, Video and Audio`

#### 🎯🎯🎯Recent Update for EduMKG 
**We sincerely thank all the reviewers for their valuable guidance on our work**
1. We have open-sourced the **RDF data of EduMKG (following IRI standards)** on Zenodo at https://zenodo.org/records/15694552.
2. We have open-sourced **an automation script for converting JSON  to RDF format in this code repository**.
3. We have released **a SPARQL endpoint** and provided **basic usage examples** in this code repository.
4. We have released the **schema** of EduMKG in this code repository .
5. We have released the **validation results for alignment quality** in this code repository.

#### EduMKG Schema
![ontology](https://github.com/user-attachments/assets/8e768d4d-f968-4cbe-84ca-6b14fccbe26c)


#### Validation Results for Alignment Quality
To validate the alignment quality, we randomly sampled 100 multimodal concepts and asked 5 volunteers to assess them. The quantitative results will be added to the paper.
| Modality       | Volunteer 1 | Volunteer 2 | Volunteer 3 | Volunteer 4 | Volunteer 5 | Average Score | 
|---------------------|-----------------|-----------------|-----------------|-----------------|-----------------|-------------------|
| Text               | 89              | 92              | 88              | 91              | 90              | 90.0             | 
| Image              | 87              | 89              | 88              | 90              | 88              | 88.4             |
| Video              | 83              | 85              | 86              | 84              | 82              | 84.0             | 
| Audio              | 89              | 92              | 88              | 91              | 90              | 90.0             | 

Key Details:  
- Volunteer Feedback: Each volunteer rated the alignment quality of multimodal concepts on a scale of 0 to 100.  
- Average Score: Arithmetic mean of scores from five volunteers.  


##### SPARQL Endpoint Url and Usage Instructions
We have open-sourced the RDF data of EduMKG on Zenodo and provided an automation script for converting JSON to RDF format in this code repository. You can execute the script by following the steps below:

1. Install `rdflib`  
```shell  
pip install rdflib  
```  

2. Configure the paths for the input JSON file and the output file, then run `rdf.py`:  
```python  
python rdf.py  
```
3. Accessing the SPARQL Endpoint and Performing Queries: We provide an example for reference.  
* Access the [Apache Jena Fuseki UI](http://103.36.221.18:46469/#/).  
* Enter the username and password: `user`, `userPassword`.  
* Example usage:
  
  Example 1
  ```sparql
  # Randomly select 10 sets of "subject-predicate-object" triplet data from the database and display them.
  PREFIX ex: <http://v1.edumkg.org/>
  SELECT ?subject ?predicate ?object
  WHERE {
  ?subject ?predicate ?object
  }
  LIMIT 10
  ```
  Example 2
   ```sparql
   # Query the concept of “上臂骨骼肌” corresponding to its explanation
   PREFIX ex: <http://v1.edumkg.org/>
   SELECT ?explanation
   WHERE {
   ?concept a ex:Concept .
   ?concept ex:hasAnExplanation ?explanation .
   FILTER(CONTAINS(STR(?concept), ENCODE_FOR_URI("上臂骨骼肌")))
   }
   ```

#### Citation
```
Lu, T. (2025). EduMKG: A Multimodal Knowledge Graph for Education with Text, Image, Video and Audio [Data set]. Zenodo. https://doi.org/10.5281/zenodo.15694552
```
---
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
