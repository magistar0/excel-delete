import random

class Modules():

    def readTextFromTxt(filepath: str):
        with open(filepath,'r',encoding="utf-8") as f:
            return f.read().strip()
        
    def writeTxtInDir(directory: str, text: str):
        with open(directory + "/result.txt",'w',encoding="utf-8") as f:
            f.write(text)

            import random
 
    def shuffleCrypto(s:str,key:int) -> str:
        random.seed(key)
        ln = len(s)
        keys = random.sample(range(ln),ln)
        out = ''
        for i in keys: out += s[i]
        return out
    
    def shuffleDecrypt(s:str,key:int) -> str:
        random.seed(key)
        ln = len(s)
        keys = random.sample(range(ln),ln)
        out = [' ' for _ in range(ln)]
        for i,j in zip(keys,s):
            out[i] = j
        return ''.join(out)
    
    def caesarCrypto(s:str,shift:int) -> str:
        m = []
        for i in s:
            if i.isalpha():
                if i.isupper():
                    m.append(chr((ord(i) + shift - 65) % 26 + 65))
                else:
                    m.append(chr((ord(i) + shift - 97) % 26 + 97))
            else:
                m.append(i)
        return ''.join(m)
    
    def caesarDecrypt(s:str,shift:int) -> str:
        return Modules.caesarCrypto(s, 26 - shift)