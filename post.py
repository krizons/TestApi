import requests
import time
import json
import random 
from model import Calc
while(True):
    r = requests.post('http://localhost:8000/calculate', params={"A":random.randint(0, 100) ,"B":random.randint(0, 100)})
    print(r.text)
    r = requests.get('http://localhost:8000/result',params=json.loads(r.text))
    print(r.text)
    time.sleep(0.1)