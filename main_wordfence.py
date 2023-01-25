import requests
import json

# CONFIGURATION #
debug_mode = True
dd_api_key = '' # need discussion
dd_schema = 'http'
dd_host = '127.0.0.1'
dd_port = '8080'
dd_user = ''
wp_fake_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'} # to bypass useragent-based restrictions

# MAIN #
def dd_get(request_url, verify = False):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(dd_api_key)}
    response = requests.get(request_url, headers=headers, verify = verify)
    return json.loads(response.content.decode('utf-8'))

def dd_get_everything(request_url, verify = False):
    response_objects = []
    while request_url:
        response = dd_get(request_url)
        response_objects.extend(response['results'])
        if response['next']:
            request_url = response['next']
        else:
            request_url = None
    
    return response_objects
    

engagements_list = dd_get_everything('{}://{}:{}/api/v2/engagements'.format(dd_schema, dd_host, dd_port))
products_list = dd_get_everything('{}://{}:{}/api/v2/products/'.format(dd_schema, dd_host, dd_port))

for product in products_list:
    for engagement in engagements_list:
        if engagement['product'] == product['id']:
            if "http" in product['description']:
                # Getting WordFence report via WF API (WF Connector) pluging
                crazy_config = product['description'].split(' ')
                if len(crazy_config) != 2:
                    if debug_mode == True:
                        print('"Invalid" description:\n\n"%s"' % product['description'])
                    break # skipping "invalid descriptions
                domain = crazy_config[0]
                wf_api_key = crazy_config[1]
                post_data = {'wf_api_command': 'list', 'wf_api_key': wf_api_key}
                try:
                    if debug_mode == True:
                        print('Trying to get a report from "%s" with API key "%s"...' % (domain, wf_api_key))
                        report = 'The request itself raised an exception and there is no way to show the report'
                    # getting final destination to send API request directly there (POST payload could be lost during HTTP redirects)
                    response = requests.get(domain, headers = wp_fake_headers, allow_redirects = True, verify = False)
                    final_destination = response.url
                    
                    # getting the report
                    report = requests.post(final_destination, headers = wp_fake_headers, data = post_data, allow_redirects = True, verify = False)
                    report_decoded = json.loads(report.content.decode('utf-8'))
                    report_dumped = json.dumps(report_decoded, indent=0)
                    if debug_mode == True:
                        print('The report is loaded:')
                        print(report_decoded)
                except:
                    print('Request failed or returned unexpected format')
                    if debug_mode == True:
                        print('Returned report (first 2048 characters):') # to not to overload logs with HTMLs
                        print(report)
                        if hasattr(report, 'text'):
                            print(report.text[:2048])
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
                    req = requests.Request('POST', "{}://{}:{}/api/v2/import-scan/".format(dd_schema, dd_host, dd_port), headers = headers, data = form_data, files = files)
                    prepared = req.prepare()
                    print('{}\n{}\r\n{}\r\n\r\n{}'.format( '-----------START-----------',
                        prepared.method + ' ' + prepared.url,
                        '\r\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
                        prepared.body
                    ))
                response = requests.post("{}://{}:{}/api/v2/import-scan/".format(dd_schema, dd_host, dd_port), headers = headers, verify = False, data = form_data, files = files)
                if debug_mode == True:
                    print(response)
                    print(response.status_code)
                    print(response.text)
                    print(response.headers)
                    print(response.url)
                break
