import requests

def getCatPr():
    headers = {"Authorization": f"token {"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"}"}
    raw_file_url = f"https://raw.githubusercontent.com/LaVida007101/reqThes/main/req"
    
    try:
        response = requests.get(raw_file_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to read file: {response.status_code} - {response.reason}")
    except Exception as e:
        print(f"Error: {e}")



def getDetPr():
    headers = {"Authorization": f"token {"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"}"}
    raw_file_url = f"https://raw.githubusercontent.com/LaVida007101/reqThes/main/reqPrtDevEv"
    
    try:
        response = requests.get(raw_file_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to read file: {response.status_code} - {response.reason}")
    except Exception as e:
        print(f"Error: {e}")

def getEvPr():
    headers = {"Authorization": f"token {"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"}"}
    raw_file_url = f"https://raw.githubusercontent.com/LaVida007101/reqThes/main/defEV"
    
    try:
        response = requests.get(raw_file_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to read file: {response.status_code} - {response.reason}")
    except Exception as e:
        print(f"Error: {e}")