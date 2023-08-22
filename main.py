import argparse
import re
import requests
from caidocsv.caidocsv import parse_csv

parser = argparse.ArgumentParser()
parser.add_argument('--caido-csv', help='Provide the path to a Caido requests and responses CSV file')

args = parser.parse_args()

if args.caido_csv:
    r_request, r_response = parse_csv(args.caido_csv)
    tld_url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    tld_response = requests.get(tld_url)
    tlds = tld_response.text.lower().splitlines()
    request_list = [element.decode('latin-1') for element in r_request]
    response_list = [element.decode('latin-1') for element in r_response]
    tld_regex = r'\b(' + '|'.join(tlds) + r')\b'
    request_map = {}
    response_map = {}
    cleaned_requests = []
    cleaned_responses = []

    for request in request_list:
        new_request = request

        for match in re.finditer(tld_regex, request, re.IGNORECASE):
            tld = match.group(0).lower()
            domain_regex = r'(?<=\.)[a-zA-Z0-9-]+(?=\.' + tld + r')'
            for domain_match in re.finditer(domain_regex, request, re.IGNORECASE):
                domain = domain_match.group(0).lower()
                
                if domain not in request_map:
                    request_map[domain] = f'example{len(request_map)}'
                clean_domain = request_map[domain]
                new_request = new_request.replace(domain + '.' + tld, clean_domain + '.' + tld)
        cleaned_requests.append(new_request)

    for response in response_list:
        new_response = response

        for match in re.finditer(tld_regex, response, re.IGNORECASE):
            tld = match.group(0).lower()
            domain_regex = r'(?<=\.)[a-zA-Z0-9-]+(?=\.' + tld + r')'
            for domain_match in re.finditer(domain_regex, response, re.IGNORECASE):
                domain = domain_match.group(0).lower()
                
                if domain not in response_map:
                    response_map[domain] = f'example{len(response_map)}'
                clean_domain = response_map[domain]
                new_response = new_response.replace(domain + '.' + tld, clean_domain + '.' + tld)
        cleaned_responses.append(new_response)
    

    