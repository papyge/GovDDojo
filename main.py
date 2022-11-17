import requests
import json
import subprocess

defect_dojo_api = '37a14e1a651856799042dc9128413053d6236f18'
url = 'http://127.0.0.1:8080/api/v2/users'
headers = {'content-type': 'application/json',
            'Authorization': 'Token {}'.format(defect_dojo_api)}

engagements = requests.get('http://127.0.0.1:8080/api/v2/engagements', headers=headers, verify=True)
engagements_list = json.loads(engagements.content.decode('utf-8'))['results']
products = requests.get('http://127.0.0.1:8080/api/v2/products/', headers=headers, verify=True)
products_list = json.loads(products.content.decode('utf-8'))['results']

print(products_list)
print(engagements_list)


for engagement in engagements_list:
    for product in products_list:
        if engagement['product'] == product['id']:
            try:
                report = requests.get(product['description'])
                report_decoded = json.loads(report.content.decode('utf-8'))
                with open('temp_file.json', 'w') as f:
                    f.write()
                domain, api = product['description'].split(' ')
                # with open('wf.json') as f:
                #     for_import = json.loads(f.read())

                headers = {'content-type': 'multipart/form-data',
                           'Authorization': 'Token {}'.format(defect_dojo_api),
                           'accept': 'application/json'}

                subprocess.run(["curl", "-X", "POST", "http://localhost:8080/api/v2/import-scan/",
                                "-H", "accept: application/json",
                                "-H","Authorization: Token 37a14e1a651856799042dc9128413053d6236f18",
                                "-H", "Content-Type: multipart/form-data",
                                "-F", "minimum_severity=Info",
                                "-F", "active=true",
                                "-F", "verified=true",
                                "-F", "scan_type=Wordfence Scan",
                                "-F", "file=@{}.json;type=application/json".format('temp_file.json'),
                                "-F", "product_name={}".format(product['name']),
                                "-F", "engagement={}".format(engagement['id']),
                                "-F", "close_old_findings=false",
                                "-F", "push_to_jira=false",
                               ])

            except Exception:
                continue
            break
