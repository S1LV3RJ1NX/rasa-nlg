from fastapi import FastAPI
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import csv,os,ast,json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dotenv import load_dotenv

load_dotenv()
