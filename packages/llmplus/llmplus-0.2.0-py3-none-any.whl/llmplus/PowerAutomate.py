from keycrypt import get_secret, set_secret
from pandas.io import clipboard
from time import sleep

from winreg import (
    CloseKey, OpenKey, QueryValueEx, SetValueEx,
    HKEY_CURRENT_USER,
    KEY_ALL_ACCESS, KEY_READ, REG_EXPAND_SZ
)
    
    
class API:
    def __init__(self):
        self.chats = []
        self.WIN_VAR_NAME = "llmState"
        self.timeout = 120
        
    def set_switch(self, state):
        key = OpenKey(HKEY_CURRENT_USER, 'Environment', 0, KEY_ALL_ACCESS)
        SetValueEx(key, self.WIN_VAR_NAME, 0, REG_EXPAND_SZ, state)
        CloseKey(key)
        
    def get_switch(self):
        root = HKEY_CURRENT_USER
        subkey = 'Environment'
        key = OpenKey(root, subkey, 0, KEY_READ)
        value, _ = QueryValueEx(key, self.WIN_VAR_NAME)
        return value
    
    def send(self, text):
        if self.get_switch() != 'PA_ready':
            raise Exception("llmService is not running!")
            
        clipboard.copy(text)
        self.set_switch("python_waiting")
        print("Wating for PA response...")
        
        c = 0
        while self.get_switch() != 'PA_done':
            c += 1
            if c > self.timeout:
                raise Exception("PA timeout")
            sleep(1)
        
        print("PA done.")
        answer = clipboard.paste()
        self.chats += [{"human": text}, {"ai": answer}]
        self.set_switch('PA_ready')
        return answer
    
    def close(self):
        self.set_switch('close')
        
        
        
if __name__ == '__main__':
    llm = API()
    answer = llm.send('what is 4+3?')
    print(answer)