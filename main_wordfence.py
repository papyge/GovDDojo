import requests
import json
import subprocess

defect_dojo_api = 'ecb3e4d1efdfa4663031f66a0d3c7a3cd07f4bc6' # change it
ip = "127.0.0.1" # change it
port = "8080" # change it
url = 'http://{}:{}/api/v2/users'.format(ip, port)
headers = {'content-type': 'application/json',
            'Authorization': 'Token {}'.format(defect_dojo_api)}
dojo_user = "" # change it
dojo_password = "" # change it

engagements = requests.get('http://{}:{}/api/v2/engagements'.format(ip, port), headers=headers, verify=False)
engagements_list = json.loads(engagements.content.decode('utf-8'))['results']
products = requests.get('http://{}:{}/api/v2/products/'.format(ip, port), headers=headers, verify=False)
products_list = json.loads(products.content.decode('utf-8'))['results']

for product in products_list:
    for engagement in engagements_list:
        if engagement['product'] == product['id']:
            request_domain_api = product['description'].split(' ')
            wordfence_request = ''.join(request_domain_api)
            report = requests.get(wordfence_request)
            report_decoded = json.loads(report.content.decode('utf-8'))
            domain, api = product['description'].split(' ')
            dumped = json.dumps(report_decoded, indent=0)
            with open('temp_file.json', 'w') as f:
                f.write(dumped)
            headers = {'content-type': 'multipart/form-data',
                           'Authorization': 'Token {}'.format(defect_dojo_api),
                           'accept': 'application/json'}

            subprocess.run(["curl", "-X", "POST", "http://{}:{}/api/v2/import-scan/".format(ip, port),
                                "-H", "accept: application/json",
                                "-H","Authorization: Token {}".format(defect_dojo_api),
                                "-H", "Content-Type: multipart/form-data",
                                "-F", "minimum_severity=Info",
                                "-F", "active=true",
                                "-F", "verified=true",
                                "-F", "scan_type=Wordfence Scan",
                                "-F", "file=@temp_file.json;type=application/json",
                                "-F", "product_name={}".format(product['name']),
                                "-F", "engagement={}".format(engagement['id']),
                                "-F", "close_old_findings=false",
                                "-F", "push_to_jira=false",
                                "-u", "{}:{}".format(dojo_user, dojo_password)
                               ])
            break

