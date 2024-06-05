import re
import requests
from hanspell import spell_checker

def getLetter(letter):
    return letter

def get_passport_key():
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
    res = requests.get(url)
    html_text = res.text
    match = re.search(r'passportKey=([^&"}]+)', html_text)
    
    if match:
        passport_key = match.group(1)
        return passport_key
    else:
        return False


def fix_spell_checker_py_code(file_path, passportKey):
    pattern = r"'passportKey': '.*'"

    with open(file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
        modified_content = re.sub(pattern, f"'passportKey': '{passportKey}'", content)
        
    with open(file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_content)
    

# before run

def speller(text):
    passport_key = get_passport_key()
    if passport_key:
        spelled_text = spell_checker.check(text)
        return spelled_text
    else:
        print("passportKey를 찾을 수 없습니다.")
        
