import requests
import json
import subprocess

defect_dojo_api = 'ecb3e4d1efdfa4663031f66a0d3c7a3cd07f4bc6' # need discussion
url = 'http://54.157.54.222:8080/api/v2/users'
headers = {'content-type': 'application/json',
            'Authorization': 'Token {}'.format(defect_dojo_api)}

engagements = requests.get('http://54.157.54.222:8080/api/v2/engagements', headers=headers, verify=True)
engagements_list = json.loads(engagements.content.decode('utf-8'))['results']
products = requests.get('http://54.157.54.222:8080/api/v2/products/', headers=headers, verify=True)
products_list = json.loads(products.content.decode('utf-8'))['results']

for product in products_list:
    for engagement in engagements_list:
        if engagement['product'] == product['id']:
            request_domain_api = product['description'].split(' ')
            wordfence_request = ''.join(request_domain_api)
            report = requests.get(wordfence_request)
            report_decoded = json.loads(report.content.decode('utf-8'))
            domain, api = product['description'].split(' ')
            print(wordfence_request)
            dumped = json.dumps(report_decoded, indent=0)
            with open('temp_file.json', 'w') as f:
                f.write(dumped)
            headers = {'content-type': 'multipart/form-data',
                           'Authorization': 'Token {}'.format(defect_dojo_api),
                           'accept': 'application/json'}

            subprocess.run(["curl", "-X", "POST", "http://54.157.54.222:8080/api/v2/import-scan/",
                                "-H", "accept: application/json",
                                "-H","Authorization: Token {}".format(defect_dojo_api),
                                "-H", "Content-Type: multipart/form-data",
                                "-F", "minimum_severity=Info",
                                "-F", "active=true",
                                "-F", "verified=true",
                                "-F", "scan_type=Wordfence Scan",
                                "-F", "file=@temp_file1.json;type=application/json",
                                "-F", "product_name={}".format(product['name']),
                                "-F", "engagement={}".format(engagement['id']),
                                "-F", "close_old_findings=false",
                                "-F", "push_to_jira=false",
                                "-u", "test:test" #need discussion
                               ])
            break

