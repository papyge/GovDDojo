import requests
import json
# CONFIGURATION #
debug_mode = False
dd_api_key = '' # need discussion
dd_schema = 'http'
dd_ip = '127.0.0.1'
dd_port = '8080'
# MAIN #
dd_headers = {'Content-Type': 'application/json',
              'Authorization': 'Token {}'.format(dd_api_key)}
engagements = requests.get('{}://{}:{}/api/v2/engagements'.format(dd_schema, dd_ip, dd_port), headers=dd_headers, verify=False)
engagements_list = json.loads(engagements.content.decode('utf-8'))['results']
products = requests.get('{}://{}:{}/api/v2/products/'.format(dd_schema, dd_ip, dd_port), headers=dd_headers, verify=False)
products_list = json.loads(products.content.decode('utf-8'))['results']
for product in products_list:
    for engagement in engagements_list:
        if engagement['product'] == product['id']:
            if "http" in product['description']:
                # Getting WordFence report via WF API (WF Connector) pluging
                domain, wf_api_key = product['description'].split(' ')
                post_data = {'wf_api_command': 'list', 'wf_api_key': wf_api_key}
                try:
                    if debug_mode == True:
                        print('Trying to get a report from "%s" with API key "%s"...' % (domain, wf_api_key))
                    report = requests.post(domain, data = post_data, verify = False)
                    report_decoded = json.loads(report.content.decode('utf-8'))
                    report_dumped = json.dumps(report_decoded, indent=0)
                except:
                    print('Request failed or returned unexpected format')
                    if debug_mode == True:
                       print(report)
                       print(report.text)
                    break
                if 'error' in report_decoded:
                    print('Resource responeded with an error: "%s"' % report_decoded['error'])
                    print('Skipping %s' % domain)
                    break
                # Sending WordFence report to DefectDojo
                headers = {'Authorization': 'Token {}'.format(dd_api_key),
                            'accept': 'application/json'}
                form_data = {"minimum_severity": "Info",
                             "active": "true",
                             "verified": "false",
                             "scan_type": "Wordfence Scan",
                             "product_name": "{}".format(product['name']),
                             "engagement": "{}".format(engagement['id']),
                             "close_old_findings": "false",
                             "push_to_jira": "false"}
                files = {'file': report_dumped}
                if debug_mode == True:
                    req = requests.Request('POST', "{}://{}:{}/api/v2/import-scan/".format(dd_schema, dd_ip, dd_port), headers = headers, data = form_data, files = files)
                    prepared = req.prepare()
                    print('{}\n{}\r\n{}\r\n\r\n{}'.format( '-----------START-----------',
                        prepared.method + ' ' + prepared.url,
                        '\r\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
                        prepared.body
                    ))
                response = requests.post("{}://{}:{}/api/v2/import-scan/".format(dd_schema, dd_ip, dd_port), headers = headers, verify = False, data = form_data, files = files)
                if debug_mode == True:
                    print(response)
                    print(response.status_code)
                    print(response.text)
                    print(response.headers)
                    print(response.url)
                break
