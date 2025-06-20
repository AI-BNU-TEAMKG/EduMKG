### EduMKG: A Multimodal Knowledge Graph for Education with Text, Video, Image and Audio
EduMKG is a multimodal educational knowledge graph dataset that covers natural sciences (biology, physics, and chemistry) in middle and high school education. It includes multimodal concepts covering text, images, videos, and audio, as well as knowledge points and exercises extracted from curriculum standards and MOOCs. EduMKG comprises 34,630 multimodal concepts and 403,400 triples, making it a vital resource for research in multimodal educational applications.

This repository contains the models and datasets described in our paper, `EduMKG: A Multimodal Knowledge Graph for Education with Text, Image, Video and Audio`

#### 🎯🎯🎯Recent Update for EduMKG 
**We sincerely thank all the reviewers for their valuable guidance on our work**
1. We have open-sourced the **RDF data of EduMKG (following IRI standards)** on Zenodo at https://zenodo.org/records/15694552.
2. We have open-sourced **an automation script for converting JSON  to RDF format in this code repository**.
3. We have provided **a detailed explanation of the ontology design and data definition of the knowledge graph**.
4. We have released **a SPARQL endpoint** and provided **basic usage examples**.

#### EduMKG ontology
![ontology](https://github.com/user-attachments/assets/8e768d4d-f968-4cbe-84ca-6b14fccbe26c)

1. **Top Level**:  
   - **Subject**: The highest-level abstraction that encapsulates a domain of knowledge.
   - Relation: `Subject relatedTo KnowledgePoint`
     - A subject is connected to multiple high-level **KnowledgePoints**.

2. **High-Mid Level**:  
   - **KnowledgePoint (High-Level)**:  Knowledge points are structured knowledge units within a discipline, serving as key nodes connecting related concepts, exercises, and other knowledge points.
   - Relation: `KnowledgePoint relatedTo KnowledgePoint`
     - High-level KnowledgePoints form hierarchical or associative relations with other KnowledgePoints, providing a structured flow of knowledge.

3. **Low-Mid Level**:  
   - **KnowledgePoint (Low-Level)**: Knowledge points are structured knowledge units within a discipline, serving as key nodes connecting related concepts, exercises, and other knowledge points.
   - Relations:
     - `KnowledgePoint relatedTo KnowledgePoint`
        - Low-level KnowledgePoints are interrelated, enabling cross-references.
     - `KnowledgePoint hasAnExercise Exercise`
        - A KnowledgePoint can be associated with an **Exercise**, which provides practice and assessment tasks.
     - `Exercise isAnExerciseOf KnowledgePoint`
        - Exercises are explicitly linked back to their corresponding KnowledgePoint.

4. **Low Level**:  
   - **Concept**: A concept represented by data from four distinct modalities.
   - Relations:
     - `KnowledgePoint relatedTo Concept`
       - KnowledgePoints are explained or supported by associated **Concepts**.
     - `Concept relatedTo KnowledgePoint`
       - Concepts can connect back to KnowledgePoints, forming bidirectional relationships.
     - `Concept hasAnExplanation Explanation`
       - A Concept can have explanatory resources to improve understanding.
     - `Concept hasA[Video|Audio|Image|Explanation]`
       - Concepts may be represented through multimedia formats, including videos, audios, images, or textual descriptions.
         
- **Explanation**: A textual description providing detail or clarification for concepts. 
  - **Relations**:  
    - `Explanation isAnExplanationOf Concept`  
      - An **Explanation** is tied to a **Concept**, offering a text-based or logical description.  
    - `Concept hasAnExplanation Explanation`  
      - A **Concept** can be explained  through an **Explanation**.
        
- **Video**: A video representation with a URL associated with concepts.
  - **Relations**:  
    - `Video isAVideoOf Concept`  
      - A **Video** is tied to a **Concept**, serving as a dynamic multimedia representation.  
    - `Concept hasAVideo Video`  

- **Audio**: An audio explanation in MP3 format associated with concepts.
  - **Relations**:  
    - `Audio isAnAudioOf Concept`  
      - An **Audio** is tied to a **Concept**, providing auditory descriptions or explanations.  
    - `Concept hasAnAudio Audio`  



##### Data Definition
| Data Type            | Definition                                                                                 | Mathematical Formalization                                |
|----------------------|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Knowledge Point      | A Knowledge point is structured knowledge unit within a discipline, serving as key node connecting related concepts, exercises, and other knowledge points. | KP = \{ id, name, associated\_concepts, associated\_knowledge_points, associated\_exercises  \}        |
| Multimodal Concept   | A concept represented by data from four distinct modalities.                              | MC = \{ id, name, T, I, V, A, associated\_knowledge\_points \}|
| Subject              | A high-level category that groups related knowledge points.                               | S = \{ id, name, associated\_knowledge\_points \}  |
| Explanation          | A textual description providing detail or clarification for concepts.                    |  T = \{ id, text\_content, associated\_concepts\}                         |
| Image                | A visual representation in PNG format associated with concepts.                         |  I = \{ id, name, associated\_concepts \}                            |
| Video                | A video representation with a URL associated with concepts.                        |  V = \{ id, url, associated\_concepts \}                                   |
| Audio                | An audio explanation in MP3 format associated with concepts.                            |  A = \{ id, name, associated\_concepts \}                           |
| Exercise             | A task or problem with a URL associated with knowledge points.        | Ex = \{ id, url, associated\_knowledge\_point \}    |
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
#### Future Work
In the future, we will update the following aspects:  
1. Expand the coverage of the dataset to include a broader range of subjects and educational stages, thereby improving its applicability and generalizability.  
2. Provide educational application research compatible with EduMKG, such as prerequisite knowledge discovery and personalized education system recommendations.  
3. Explore more efficient model designs to refine the proposed methods and broaden their practical applications in educational contexts.
   
We look forward to the research community further exploring and utilizing this dataset to advance education and applied research related to multimodal educational knowledge graphs.

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
