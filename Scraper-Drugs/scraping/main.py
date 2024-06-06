import importlib 
import sys
import json


def default():
    module = sys.argv[1]
    print(sys.argv)
    try:
        scraper = importlib.import_module(f"scraping.drugs.main")
        # entry_point = getattr(scraper, 'default')
        # result = entry_point([5])     
         
        # with open('z_file/drug_info.json', 'w', encoding='utf-8') as file:
        #     json.dump(result, file, ensure_ascii=False, indent=4)
    except:
        print(f"module {module} not found")
