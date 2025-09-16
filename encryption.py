def vigenere_encrypt(text: str, key: str) -> str:
    encrypted = []
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if char.islower():
                encrypted.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                encrypted.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            key_index += 1
        else:
            encrypted.append(char)
    return "".join(encrypted)

def vigenere_decrypt(text: str, key: str) -> str:
    decrypted = []
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if char.islower():
                decrypted.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            else:
                decrypted.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            key_index += 1
        else:
            decrypted.append(char)
    return "".join(decrypted)

SECRET_KEY = "securechat"  # مفتاح التشفير (غيره إذا حبيت)

def encrypt_message(msg: str) -> str:
    return vigenere_encrypt(msg, SECRET_KEY)

def decrypt_message(msg: str) -> str:
    return vigenere_decrypt(msg, SECRET_KEY)
