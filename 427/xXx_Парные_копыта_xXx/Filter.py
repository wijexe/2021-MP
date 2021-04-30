def filter_text(text):
    text = text.lower()
    text = [c for c in text if c in "123456789йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm"]
    text = ''.join(text)
    return text


class Filter():
    def showBanList(self):
        with open('banWords.txt', encoding='utf-8') as f:
            ban = f.read().splitlines()
        return ban

    def censor(self, text):
        for word in str(text.splitlines()).strip('[\']').split(' '):
            for ban_word in self.showBanList():
                if filter_text(word) == ban_word:
                    text = text.replace(word, "****")
        return text
