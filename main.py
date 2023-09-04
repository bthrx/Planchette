import argparse
import re
import requests
from openai_request.openai import openai_request
from caidocsv.caidocsv import parse_csv

planchette= """
                                    :^
                                  :!^^^!:.
                               .:!^:  ..~~^.
                             .^!~.       .~^~.
                           .~~~            .^~!.
                          ~~~.               .:!^.
                        ^!^.  ~~     .:       ..:!^:
                     .:7^.    .~~    ^!       !~  ^~~.
                    :!~.       :~^   ^~     ~!     .~~~
                  :~!.  :.      :!~.!!~!.^^!:.       :^!^
                .~!^   .!^ :: :~!:~.:..:.~^?^. . .!.   :^!.
               ^!^         ~~~!.           .:!^7:.^.    .:7^.
             .!~: .^. ..    !~               :7:          .~!:
            ^7:   :!..!^ ^~:7.                ~!..  .  ..   :!^.
          .!~.           ::^7.                !~^! :7..7:     ~~^
         :7^      ^:       .7^               ^7.               :!~.
        ^7:       ~^       !~!~.           .!~!! .:             .!~:
       ~7.  .:          ~! . .:?:~:.. . ^:!~:.:: ^!.        ~!    ~~:
      ~!.   .:          .     :7:^:~~^7:~~7:                ..     ^!:
     ~!.                     ~!     ^!    .:!.          ~.          ^!^
    ^7.            ^:      .!^.     ~!     .^:^                      ^!^
   :7:      .:              ^.      ..       ^~                       ^!:
   !~       :!                                             .:   .:     ~!.
  ^!.       ^!.       .:                           :^      ~~   .:      !~
 .7^     .~~~^~^      :!.              !~:~                         .:  :7:
 ^7.       :~~:.             ^^   ^!   . :^^~:^                     .:   ~!
!~         !.                    ..       ::?!~.         :              :7:
:7:        .^      .:                        ~!~!.   !^  .^.              !~
^!.                ::           :.           ^7:7^   :.       ^.     .:   ~!
~!  .^                   .~.   :!:    .~     ~!.7^            :.     ^~   ^7
~~   .       .       .   .7~           .    :7:.7:       .:               ^7
~!          .~.     ~!    ^~~.            .~!^.!~   .^   .!^.       .:    ~!
:7.                        :J^7:^....:.^:!~^.:!~    .:   :~~~       .^    7^
 !!   .!:                   :~!^7:!^:!.~:^.~^~:            !:            ^7.
 .~!. .:.      ..      ^.    ..:~:7:!^:!:!::.    ^.                     :7^
  .~!.         ^.      :          . :...        .~:  :^        ::      :!^
   .^!~..                     .: ^:.!::7.:!...       ..   ^!   ..    :~!:
     ..!^^^.: .    . ...^.~:!~^!.~: :  . .:.!~~~.~.:. . . .:     .::!^^
       ^:^!:7:~~:7:!^^~.^...                ...~.!^^!:7:!~:7:!^^~.:
    ______ _       ___   _   _ _____  _   _  _____ _____ _____ _____
    | ___ \ |     / _ \ | \ | /  __ \| | | ||  ___|_   _|_   _|  ___|
    | |_/ / |    / /_\ \|  \| | /  \/| |_| || |__   | |   | | | |__
    |  __/| |    |  _  || . ` | |    |  _  ||  __|  | |   | | |  __|
    | |   | |____| | | || |\  | \__/\| | | || |___  | |   | | | |___
    \_|   \_____/\_| |_/\_| \_/\____/\_| |_/\____/  \_/   \_/ \____/
"""
print(planchette)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--caido-csv", help="Provide the path to a Caido requests and responses CSV file"
)
parser.add_argument(
    "--llm", choices=["openai"], default="openai", help="Select LLM to use."
)
parser.add_argument("--output", type=str, help="Output file path")
args = parser.parse_args()

if args.caido_csv:
    r_request, r_response = parse_csv(args.caido_csv)
    tld_file = open('tlds-alpha-by-domain.txt','r')
    tlds = tld_file.read().lower().splitlines()
    request_list = [element.decode("latin-1") for element in r_request]
    response_list = [element.decode("latin-1") for element in r_response]
    tld_regex = r"\b(" + "|".join(tlds) + r")\b"
    request_map = {}
    response_map = {}
    cleaned_requests = []
    cleaned_responses = []

    for request in request_list:
        new_request = request

        for match in re.finditer(tld_regex, request, re.IGNORECASE):
            tld = match.group(0).lower()
            domain_regex = r"(?<=\.)[a-zA-Z0-9-]+(?=\." + tld + r")"
            for domain_match in re.finditer(domain_regex, request, re.IGNORECASE):
                domain = domain_match.group(0).lower()

                if domain not in request_map:
                    request_map[domain] = f"example{len(request_map)}"
                clean_domain = request_map[domain]
                new_request = new_request.replace(
                    domain + "." + tld, clean_domain + "." + tld
                )
        cleaned_requests.append(new_request)

    for response in response_list:
        new_response = response

        for match in re.finditer(tld_regex, response, re.IGNORECASE):
            tld = match.group(0).lower()
            domain_regex = r"(?<=\.)[a-zA-Z0-9-]+(?=\." + tld + r")"
            for domain_match in re.finditer(domain_regex, response, re.IGNORECASE):
                domain = domain_match.group(0).lower()

                if domain not in response_map:
                    response_map[domain] = f"example{len(response_map)}"
                clean_domain = response_map[domain]
                new_response = new_response.replace(
                    domain + "." + tld, clean_domain + "." + tld
                )
        cleaned_response_headers = new_response.split('\r\n\r\n')[0]
        cleaned_responses.append(cleaned_response_headers)

if args.llm == "openai":
    ai_messages = openai_request(cleaned_requests, cleaned_responses)

#    if args.output:
#        with open(args.output, "w") as f:
#                f.write(ai_messages)
#    else:
#        for message in ai_messages:
#            print(message)
