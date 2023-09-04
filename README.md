# Planchette
AI tool to help make sense of all your proxied traffic. Currently it only works with a Caido CSV file and with the openai LLM.

### Install:
Install requirements.txt

### Use:
Put your OpenAI api key in config/keys.ini 
```python main.py --caido-csv /PATH/TO/CSV --llm openai | tee /PATH/TO/SAVE/FILE```

### Limitations:
Results are a mixed bag. I have tested it against a few CTF's I am familiar with and it suggests the correct vulnerability to test for on the appropriate request and response pair. This isn't a tool to identify vulnerabilities but as a way to help you make sense of what you should test for. Currently it is using zero-shot prompting, but am working on developing prompts to implement few-shot prompts to get better results. 

### Another thing to note:
Currently Planchette uses a regex to identify root domains and change them to example0, example1, example2, etc. to help bypass guardrails. It does not change them back at this time to the correct root domain. It does create a dictionary to sort through them so the pairs are saved but I need to implement changing them back to the correct domain.
