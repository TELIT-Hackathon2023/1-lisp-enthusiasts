import requests
import json

line = "https://marian.mach.website.tuke.sk/"
#line = "https://www.orange.sk/"
x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}'
print(f'Requesting {x}...')

r = requests.get(x)
final = r.json()
#print(final["loadingExperience"]["metrics"])
    

"""
for k, v in final['lighthouseResult']['audits'].items():
    try:
       if(v["score"] < 1):
              print(v["title"])
              print(v["description"])
              print(v["displayValue"])
              print(v["score"] * 100 + '%')
              print('-------------------------------------------------------')
    except:
          
         try: 
            print(v["displayValue"])
         except:
               print("KEY: " + k)
with open("sample_audit.json", "w") as outfile:
    json.dump(final['lighthouseResult']['audits'], outfile)
try:
        urlid = final['id']
        split = urlid.split('?') # This splits the absolute url from the api key parameter
        urlid = split[0] # This reassigns urlid to the absolute url
        ID = f'URL ~ {urlid}'
        ID2 = str(urlid)
        urlfcp = final['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
        FCP = f'First Contentful Paint ~ {str(urlfcp)}'
        FCP2 = str(urlfcp)
        urlfi = final['lighthouseResult']['audits']['interactive']['displayValue']
        FI = f'First Interactive ~ {str(urlfi)}'
        FI2 = str(urlfi)
except KeyError:
        print(f'<KeyError> One or more keys not found {line}.')

try:
        print(ID) 
        print(FCP)
        print(FI)
except NameError:
        print(f'<NameError> Failing because of KeyError {line}.')

"""