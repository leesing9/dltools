from cryptography.fernet import Fernet, InvalidToken # symmetric encryption

class Crypt:
    def __init__(self):
        self.key = b'ch-XAHMaHfaeLprYdCIzT21oRnqQ0cMs2h0-Y0GXw5E=' # 키를 생성한다
        self.f   = Fernet(self.key)
    
    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data) # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8')) # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou
        
    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data) # 바이트형태이면 바로 복호화
        else:
            try:
                ou = self.f.decrypt(data.encode('utf-8')) # 인코딩 후 복호화
            except InvalidToken:
                return ''
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou


if __name__ == "__main__":
    simpleEnDecrypt = Crypt()
    plain_text = 'hello crypto world'
    print(plain_text)
    encrypt_text = simpleEnDecrypt.encrypt(plain_text)
    print(encrypt_text)
    decrypt_text = simpleEnDecrypt.decrypt(encrypt_text)
    print(decrypt_text)