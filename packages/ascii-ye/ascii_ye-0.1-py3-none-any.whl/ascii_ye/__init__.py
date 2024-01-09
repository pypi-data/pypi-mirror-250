# library by SaMi_ye 
# Version python 3
class ASCII_YE:
    @staticmethod
    def encrypt(text):
        ascii_values = [ord(char) for char in text]
        encrypted_text = ','.join(map(str, ascii_values))
        return encrypted_text

    @staticmethod
    def decrypt(encrypted_text):
        ascii_values = list(map(int, encrypted_text.split(',')))
        decrypted_text = ''.join(chr(value) for value in ascii_values)
        return decrypted_text
