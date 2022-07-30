import sys
import json
import requests

baseUrl = "https://api.pagerduty.com"
token = "u+MZZXxTg281-qCrdoyQ"

print()




uri = f"{baseUrl}/users"
headers = {
    "Authorization": f"Token token={token}",
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Content-Type" : "application/json"
}

result = requests.get(uri, headers=headers)
if (result.status_code == 200):
	print(f"HTTP {result.status_code}")
	data = result.json()



#print(data)

	name = []
	user_id =[]
#iterate over user ids

	for id in data['users']:
		user_id.append(id['id'])
		name.append(id['name'])

#if (result.status_code == 200):
#     print (json.dumps(result.json(), indent=4, sort_keys=True))

    
    #for id in data['id']:
#	print(id)


####use the sessions id from user_list to retrieve last login time
	last_login = []

	for i in user_id:

		uri = f"{baseUrl}/users/{i}/sessions"
		headers = {
    		"Authorization": f"Token token={token}",
    		"Accept": "application/vnd.pagerduty+json;version=2",
    		"Content-Type" : "application/json"
		}

		result = requests.get(uri, headers=headers)
		data = result.json()
		login = []
	
		if len(data['user_sessions']):
			for t in data['user_sessions']:
				login.append(t['created_at'])
			last_login.append(login[-1])
		else:
			last_login.append("null")

	dicts = {}


	for i in range(len(name)):
		dicts[name[i]] = last_login[i]
	
	import csv
    
	with open('user_sessions.csv', 'w', newline='') as csvfile:
   		header_key = ['User_Name', 'Last_Login']
   		new_val = csv.DictWriter(csvfile, fieldnames=header_key)
   		new_val.writeheader()
   		
   		for new_k in dicts:
   			new_val.writerow({'User_Name': new_k, 'Last_Login': dicts[new_k]})
	

else:
	print(result.reason)