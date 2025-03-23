import json
import csv
import os
from typing import List, Dict, Any


def save_to_json(data: List[Dict[str:Any]], filename:str) -> None:
    
    if not data:
        return 
    
    os.makedirs('output', exist_ok= True)
    
    with open(f'output/{filename}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=2)
        
def save_to_csv(data: List[dict[str:Any]], filename:str) -> None:
    
    if not data:
        return
    
    os.makedirs('output',exist_ok=True)
    
    with open(f'output/{filename}', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        