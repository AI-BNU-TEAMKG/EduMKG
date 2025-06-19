### EduMKG: A Multimodal Knowledge Graph for Education with Text, Video, Image and Audio
EduMKG is a multimodal educational knowledge graph dataset that covers natural sciences (biology, physics, and chemistry) in middle and high school education. It includes multimodal concepts covering text, images, videos, and audio, as well as knowledge points and exercises extracted from curriculum standards and MOOCs. EduMKG comprises 34,630 multimodal concepts and 403,400 triples, making it a vital resource for research in multimodal educational applications.

This repository contains the models and datasets described in our paper, `EduMKG: A Multimodal Knowledge Graph for Education with Text,  Image, Video and Audio`

#### 🎯🎯🎯Recent Update for EduMKG 
**We sincerely thank all the reviewers for their valuable guidance on our work**

##### EduMKG ontology

##### Data Definition
| Data Type            | Definition                                                                                 | Mathematical Formalization                                |
|----------------------|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Knowledge Point      | The core facts, skills, or principles of a specific discipline, potentially linked to other concepts and Knowledge Points. | KP = \{ id, name, associated\_concepts, associated\_knowledge points \}        |
| Multimodal Concept   | A concept represented by data from four distinct modalities.                              | MC = \{ id, name, T, I, V, A, associated\_knowledge\_points \}, where \( T,I,V,A \) represents a specific modality's data. |
| Subject              | A high-level category that groups related knowledge points.                               | S = \{ id, name, associated\_knowledge\_points \}  |
| Explanation          | A textual description providing detail or clarification for a concept.                    |  T = \{ id, text\_content, associated\_concepts\}                         |
| Image                | A visual representation in PNG format associated with a concept.                         |  I = \{ id, name,associated\_concepts \}                            |
| Video                | A video representation with a URL link associated with a concept.                        |  V = \{ id, URL,associated\_concepts \}                                   |
| Audio                | An audio explanation in MP3 format associated with a concept.                            |  A = \{ id, name, associated\_concepts \}                           |
| Exercise             | A task or problem with a URL link for practice or assessment related to a concept.        | Ex = \{ id, url, associated\_knowledge\_point \}    |
##### SPARQL Endpoint Url and Usage Instructions



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
