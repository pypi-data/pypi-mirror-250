# llmplus
Usage
```python
from llmplus.ChatGot.api import API, Models
authorization_key = 'your authorization key from website headers'
api = API(authorization_key)
    
api.model = Models.GPT4()
answer = api.send('who is the manager of the real madrid?')

asnwer2  = api.send('who is the CEO?')
```

Models
```python
Models.GPT4
Models.GPT3
Models.Claude2
```

Acsess to the chat history
```python
API.json_data['messages']
```

Extracting code block
set extract_code to the type of code block to return just the code block

asnwer2  = api.send('who is the CEO?', extract_code = "json")

LLM output:
#=====================
your output is here
```json
{"a": "ssdgs"}
```
#=====================

LLM output with extract_code:
#=====================
{"a": "ssdgs"}
#=====================




