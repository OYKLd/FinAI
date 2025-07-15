import requests

API_URL = "http://localhost:8000/generate-report"  # à adapter si déployé ailleurs

def send_file_for_report(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post(API_URL, files=files)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête API : {e}")
        return None