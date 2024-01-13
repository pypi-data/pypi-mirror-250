import requests
from json import loads
from . import Models


def headers(authorization):
    h = {
        'Accept': '*/*',
   'Accept-Language': 'en-US,en;q=0.9',
   'Authorization': authorization,
   'Connection': 'keep-alive',
   'Origin': 'https://start.chatgot.io',
   'Referer': 'https://start.chatgot.io/',
   'Sec-Fetch-Dest': 'empty',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Site': 'same-site',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
   'content-type': 'application/json',
   'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
   'sec-ch-ua-mobile': '?0',
   'sec-ch-ua-platform': '"Windows"',
       }
    return h

class API:
    def __init__(self, authorization_key):
        self.authorization_key = authorization_key
    
        self.json_data = {
            'model': {
                'id': 'openai/gpt-4',
                'name': 'openai/gpt-4-1106-preview',
                # 'title': 'GPT-4',
                # 'icon': '/assets/imgs/icon/4.jpg',
                # 'extra': {
                #     'title': '128k',
                #     'bgColor': '#000',
                # },
                # 'placeholder': '',
                # 'description': "The latest GPT-4 model, which is currently the world's most outstanding large language model, provided by OpenAI, can offer you high-quality answers in various aspects. It can return up to 4,096 output tokens and has a maximum context window of 128,000 tokens.",
                'order': 0,
                'unused': False,
                'isActived': True,
                'value': 'GPT-4 128k',
                'isReplying': True,
                'prompt': ''
            },
            'messages': [],
        }
    
        self.model = Models.GPT4()
    def send(self, prompt, extract_code = None):
        self.json_data['messages'] += [{
            'role': 'user',
            'content': prompt,
        }]
        
        
        for key in self.model.json:
            self.json_data['model'][key] = self.model.json[key]
    
        while True:
            try:
                response = requests.post('https://api.chatgot.io/api/chat/conver', 
                                         headers=headers(self.authorization_key), 
                                         json=self.json_data)
                if response.status_code not in [200, 201]:
                    print('status' ,response.status_code)
                    print(response.content)
                
                lines=response.text.split('\n\ndata:')
                answer = ''.join([loads(x)['choices'][0]['delta']['content'] for x in lines[1:-2]])
                break
            except Exception as e:
                print(e)
                
        if extract_code is not None:
            try:
                if '```' in answer:
                    answer = answer.split('```')[1].replace(extract_code, '')
                else:
                    answer = '{' + ('}'.join(('{'.join(answer.split('{')[1:]).split('}')[:-1]))) + '}'
                print('extract_code done.')
            except:
                print('failed to extract_code')
                
                
        self.json_data['messages'] += [{
            'role': 'assistant',
            'content': answer,
        }]
        
        return answer
    
if __name__ == '__main__':
    authorization_key = 'authorization_key'
    api = API(authorization_key)
    
    api.model = Models.Claude2()
    answer = api.send('who is the manager of the real madrid?')
    
    # asnwer2  = cg.send('who the CEO?')
