import base64
import csv

def parse_csv(file_path):
    requests = []
    responses = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            request = base64.b64decode(row['raw'])
            response = base64.b64decode(row['response_raw'])
            requests.append(request)
            responses.append(response)
    return requests, responses