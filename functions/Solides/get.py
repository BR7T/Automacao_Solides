import os
import requests


def GetAllSolidesPontos(page , dia):    
    headerAPIKey = {
        "Authorization":f"Basic {os.getenv("APIKEY_SOLIDES")}"
    }
    url = f"https://apis.tangerino.com.br/punch/?size=500&page={page}&startDate={dia}"
    # url = f"https://apis.tangerino.com.br/punch/?size=500&page={page}"

    resp = requests.get(url , headers=headerAPIKey)
    data = resp.json()
    return data
 
def _GetAllEmployeesAndWorkPlace_():
    headerAPIKey = {
        "Authorization":f"Basic {os.getenv("APIKEY_SOLIDES")}"
    }
    urlWorkPlace = "https://employer.tangerino.com.br/workplace/find-all?size=1000"
    urlEmployees = "https://employer.tangerino.com.br/employee/find-all?size=1000"
    respWork = requests.get(urlWorkPlace , headers=headerAPIKey)
    respEmpl = requests.get(urlEmployees , headers=headerAPIKey)

    dataEmpl = respEmpl.json()
    dataWork = respWork.json()
    return dataEmpl , dataWork

   
    


