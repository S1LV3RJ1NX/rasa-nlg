from package_imports import *

class GSheet:

    SERVICE_FILE_KEY = os.getenv('GSHEET_KEY') # google api env key
    SPREADSHEET = 'NLG Responses'
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    @staticmethod
    def create_nlg_data(worksheet_idx):

        creds_dict = json.loads(GSheet.SERVICE_FILE_KEY)
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, GSheet.scope)
        client = gspread.authorize(creds)

        sheet = client.open(GSheet.SPREADSHEET)
        sheet_instance = sheet.get_worksheet(worksheet_idx)
        records = sheet_instance.get_all_records()

        nlg_dict = {}

        for dict_obj in records:
            key = dict_obj['utterance']
            nlg_dict[key] = dict_obj

        return nlg_dict

    def __init__(self, worksheet_idx):
        self.nlg_data = GSheet.create_nlg_data(worksheet_idx)

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