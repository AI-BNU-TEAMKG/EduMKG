import wikipediaapi
import time
import requests
from Translate import *
def get_wikipedia_summary(concept: str, language="en") -> str:

    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }


    wiki = wikipediaapi.Wikipedia(
        language=language
    )  


    session = requests.Session()
    session.proxies = proxies
    session.headers.update({
        "User-Agent": "MyWikipediaBot/1.0 (https://example.com; myemail@example.com)"
    })


    wiki._session = session

    summaries = {}
    max_retries = 5
    retry_delay = 2

    translated_term = baidu_translate(concept)  

    for attempt in range(max_retries + 1):
        try:
            page = wiki.page(translated_term)
            if page.exists():
                summaries[concept] = page.summary
                print(f"  '{concept}'  ✅")
                break
            else:
                summaries[concept] = "not found"
                print(f"❌ '{translated_term}'")
                break
        except Exception as e:
            error_msg = f" {attempt + 1}/{max_retries} : {str(e)}"
            print(error_msg)
            if attempt < max_retries:
                time.sleep(retry_delay * (2 ** attempt))  # 
    else:
        summaries[concept] = "error"
        print(f"⚠️  {max_retries}，")
    
    return summaries