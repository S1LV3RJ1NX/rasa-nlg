# creating gsheet api: https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
# from package_imports import *
from classes import *

app = FastAPI()

# WORKSHEET_INDICES
PORTFOLIO_WORKSHEET_IDX = 1

# NLG OBJECTS
portfolio_nlg_model = GSheet(PORTFOLIO_WORKSHEET_IDX)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# PORTFOLIO ROUTE
@app.post("/portfolio")
async def portfolio_bot_utterance(nlg_req: NLG_request):
    bot_response = await portfolio_nlg_model.search_record(nlg_req)
    return bot_response 


