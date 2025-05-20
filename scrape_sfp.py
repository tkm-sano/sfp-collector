
import os, json, time, requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2 import service_account

def main():
    creds = service_account.Credentials.from_service_account_info(
        json.loads(os.environ["GCP_SERVICE_ACCOUNT_JSON"]),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    sheet  = build("sheets", "v4", credentials=creds).spreadsheets()
    sid    = os.environ["SPREADSHEET_ID"]
    urls   = ["https://example.com/sf-prototyping"]
    rows   = []
    for u in urls:
        try:
            s = BeautifulSoup(requests.get(u, timeout=5).text, "html.parser")
            title = s.title.string if s.title else "No Title"
            desc  = (s.find("meta", {"name":"description"}) or {}).get("content","")
            rows.append([u, title, desc])
        except Exception as e:
            rows.append([u, "Error", str(e)])
        time.sleep(1)
    sheet.values().append(
        spreadsheetId=sid, range="Sheet1!A1",
        valueInputOption="RAW", body={"values": rows}
    ).execute()
if __name__ == "__main__":
    main()
