from oauth2client.service_account import ServiceAccountCredentials
import gspread


def get_google_sheet():
    """Returns the google sheet used to store mix metadata."""
    gspread_client = gspread.authorize(
        ServiceAccountCredentials.from_json_keyfile_name(
            '/data/google_api_client_secret.json', [
                'https://www.googleapis.com/auth/drive',
                'https://spreadsheets.google.com/feeds',
            ]
        )
    )
    return gspread_client.open('Midnight Athletics Radio Data').sheet1
