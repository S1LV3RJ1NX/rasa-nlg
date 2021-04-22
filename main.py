# creating gsheet api: https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/

from fastapi import FastAPI
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import csv,os,ast,json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dotenv import load_dotenv

load_dotenv()

SERVICE_FILE_KEY = os.getenv('GSHEET_KEY') #google api file
SERVICE_FILE = 'nlg-service.json'
SPREADSHEET = 'NLG Responses'
WORKSHEET_IDX = 1 # worksheet index starting from zero

class GSheet:

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    @staticmethod
    def create_nlg_data(spreadsheet_name, worksheet_idx):

        creds_dict = json.loads(SERVICE_FILE)
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, GSheet.scope)
        # creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_FILE, GSheet.scope)
        client = gspread.authorize(creds)

        sheet = client.open(spreadsheet_name)
        sheet_instance = sheet.get_worksheet(worksheet_idx)
        records = sheet_instance.get_all_records()

        nlg_dict = {}

        for dict_obj in records:
            key = dict_obj['utterance']
            nlg_dict[key] = dict_obj

        return nlg_dict

    def __init__(self, spreadsheet_name, worksheet_idx):
        self.nlg_data = GSheet.create_nlg_data(spreadsheet_name, worksheet_idx)

    async def search_record(self, nlg_request):
        nlg_response = {
            "text": "",
            "buttons": [],
            # "image": "",  # string of image URL
            # "elements": [],
            # "attachments": [], 
            "custom": {}
        }
        
        key = nlg_request.response
        args = nlg_request.arguments

        if self.nlg_data.get(key):

            response_type = 'english_response'
            if self.nlg_data.get(key,None):
                utter_dict = self.nlg_data.get(key)
                text = utter_dict.get(response_type)
                args_list = list(args.keys())
        
                if len(args_list) == 0:
                    nlg_response["text"] = text
                else:
                    text = text.format(**args)
                    nlg_response["text"] = text
                

                if utter_dict.get('buttons',''):
                    nlg_response['buttons'] = ast.literal_eval(utter_dict.get('buttons'))

                if utter_dict.get('image',''):
                    nlg_response['image'] = utter_dict.get('image','')
        else:
            nlg_response['text'] = 'Utterance not found'
        
        return nlg_response

    
class NLG_request(BaseModel):
    response: str
    arguments: Optional[dict] = None
    tracker: dict
    channel: Optional[dict] = None

app = FastAPI()
nlg_model = GSheet(SPREADSHEET, WORKSHEET_IDX)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.post("/nlg")
async def bot_utterance(nlg_req: NLG_request):

    
    bot_response = await nlg_model.search_record(nlg_req)
    return bot_response 


