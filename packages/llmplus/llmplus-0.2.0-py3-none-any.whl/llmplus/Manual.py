from pandas.io import clipboard

class Manual:
    def __init__(self):
        self.chats = []
        
    def send(self, text, extract_code = None):
        clipboard.copy(text)
        print("Prompt added to clipboard.")
        answer = input("Enter the anwer:")
        self.chats += [{"human": text}, {"ai": answer}]
        return answer