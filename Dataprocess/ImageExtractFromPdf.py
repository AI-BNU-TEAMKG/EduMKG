import requests
from bs4 import BeautifulSoup


file_path = r""


url = ""


payload = {
    "format": "png",
    "allowDuplicates": "false"
}

files = {
    "fileInput": (file_path, open(file_path, "rb"), "application/pdf")
}


response = requests.post(url, headers={"accept": "*/*"}, data=payload, files=files)


if response.status_code == 200:
  
    content_disposition = response.headers.get("content-disposition")
    filename = ""  

    if content_disposition:
      
        parts = content_disposition.split(";")
        for part in parts:
            if "filename=" in part:
                filename = part.split("=")[1].strip().strip('"')  

    with open("", "wb") as f:
        f.write(response.content)
    
    print(f": {filename}")
else:
    print(f" {response.status_code}")
    