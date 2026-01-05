import requests
from bs4 import BeautifulSoup
import json
import datetime

def parse_status():
    url = "https://alerts.org.ua/kyiv/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        groups = soup.find_all(class_='js-group')

        for group in groups:
            group_id = group.get('data-group-id')
            group_name = group.find(class_='group-name').get_text(strip=True)
            active_block = group.find(class_='active')
            
            status_info = None
            if active_block:
                is_powered = "stts0" in active_block.get('class', [])
                status_tag = active_block.find('b')
                time_range = active_block.get_text(strip=True).replace(status_tag.get_text(), "").strip() if status_tag else ""
                
                status_info = {
                    "status": "ON" if is_powered else "OFF",
                    "time_range": time_range,
                    "is_powered": is_powered
                }

            results.append({
                "group_id": group_id,
                "group_name": group_name,
                "current": status_info
            })

        data = {
            "last_updated": datetime.datetime.now().isoformat(),
            "groups": results
        }

        with open('status.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse_status()