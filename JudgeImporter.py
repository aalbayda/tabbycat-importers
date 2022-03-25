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
                           sheet_name='IAs')

for k in sheet['Name']:    
    name = sheet['Name'][x]
    score = 0
    email = sheet['Email'][x]
    number = 0
    gender = ""

    code = sheet['Code'][x]
    print(code)
    if code == "Unaffiliated":
        institution = None
    else:
        for i in institutions:
           if i['code'] == code:
            institution = i['url']
            break

    x = x+1

    r = requests.post(
        f'{site}api/v1/tournaments/{slug}/adjudicators',
        json = {
        "name": name,
        "email": email,
        "anonymous": False,
        "institution": institution,
        "base_score": float(score),
        "breaking": False,
        "trainee": False,
        "independent": True,
        "adj_core": False,
        "institution_conflicts": [],
        "team_conflicts": [],
        "adjudicator_conflicts": [],
        "gender": gender
        },
        headers={
                'Authorization': 'token '+token
                })

    status = r.status_code
    print(f"{status}: {name}")
    if status != 201:
        print(f"Error occured while posting {name}, {code}\n Error {status}\n{r.text}")
        
x = input()
