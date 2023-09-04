from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,SystemMessagePromptTemplate, HumanMessagePromptTemplate
from config.config import get_api_key
from langchain.schema.output_parser import StrOutputParser

def openai_request(cleaned_requests, cleaned_responses):
    api_key = get_api_key('openai')
    chat = ChatOpenAI(openai_api_key=api_key)
    system_template = "You are an expert at web application security and can look at requests and responses and give suggestions on what might be vulnerable using the knowledge of OWASP, CWE's and CVE's. Your responses will show the URL and what part of the request and response is vulnerable."
    human_template = "I have this {cleaned_request} and this {cleaned_response}. Using your knowledge from bug bounty reports, OWASP Testing Guides, CWE's and CVE's, please give me advice on what is potentially vulnerable and needs to be tested." 
    system_message = SystemMessagePromptTemplate.from_template(system_template)
    human_message = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    for i in range(len(cleaned_requests)):
        prompt = chat_prompt.format_messages(cleaned_request=cleaned_requests[i], cleaned_response=cleaned_responses[i])
        results = chat(prompt)
        print('Request:\n'+cleaned_requests[i]+'\r\n\r\n'+'Response:\n'+cleaned_responses[i]+'\r\n\r\n'+'Suggestions:\n'+results.content+'\n')