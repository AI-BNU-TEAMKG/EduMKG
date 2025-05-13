### EduMKG: A Multimodal Knowledge Graph for Education with Text, Video, Image and Audio
EduMKG is a multimodal educational knowledge graph dataset that covers natural sciences (biology, physics, and chemistry) in middle and high school education. It includes multimodal concepts covering text, images, videos, and audio, as well as knowledge points and exercises extracted from curriculum standards and MOOCs. EduMKG comprises 34,630 multimodal concepts and 403,400 triples, making it a vital resource for research in multimodal educational applications.

This repository contains the models and datasets described in our paper, `EduMKG: A Multimodal Knowledge Graph for Education with Text,  Image, Video and Audio`

#### Dataset and Models
* `Dataset`: All information about EduMKG data is at https://zenodo.org/records/15386565, including extracted raw data from MOOCs and generated EduMKG.
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
