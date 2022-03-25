import pandas as pd
import requests

site = "https://luzonintervarsity.calicotab.com/"
token = "[insert token here]"
slug = "liv2021"


print("Getting the institution data...")
r = requests.get(
        f'{site}api/v1/institutions',
        headers={
                'Authorization': 'token '+token
                })
                 
institutions = r.json()

x=0
sheet = pd.read_excel(open('tab_database.xlsx', 'rb'),
                           sheet_name='new')

for k in sheet['Team']:
    
    name = sheet['Team'][x]
    code = sheet['Code'][x]    
    for i in institutions:
        if i['code'] == code:
            institution = i['url']
            break
    short = sheet['Short'][x]
    
    S1 = sheet['S1'][x]
    E1 = sheet['E1'][x]
    N1 = sheet['N1'][x]
        
    S2 = sheet['S2'][x]
    E2 = sheet['E2'][x]
    N2 = sheet['N2'][x]
    
    x = x+1
    
    r = requests.post(
        f'{site}api/v1/tournaments/{slug}/teams',
        json = {
  "reference": name,
  "short_reference": short,
  "institution": institution,
  "speakers": [
    {
      "name": S1,
      "gender": "",
      "email": E1,
      "phone": 0,
      "anonymous": False,
      "pronoun": "",
      "categories": [site+"api/v1/tournaments/"+slug+"/speaker-categories/1"] if N1 == "Yes" else [],
      "url_key": ""
    },
    {
      "name": S2,
      "gender": "",
      "email": E2,
      "phone": 0,
      "anonymous": False,
      "pronoun": "",
      "categories": [site+"api/v1/tournaments/"+slug+"/speaker-categories/1"] if N2 == "Yes" else [],
      "url_key": ""
    }
  ],
  "use_institution_prefix": False,
  "break_categories": [site+"api/v1/tournaments/"+slug+"/break-categories/3"] if N1 == "Yes" and N2 == "Yes" else [],
  "institution_conflicts": []
},
        headers={
                'Authorization': 'token '+token
                })
    print(f"{name}")
    status = r.status_code
    if status != 201:
        print(f"Error occured while posting {name}\n Error {status}\n{r.text}")
        
x = input("Importing is done successfully! Press any key to continue...")
