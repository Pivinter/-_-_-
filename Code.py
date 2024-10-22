import os
import time
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


# Генерація виклику
def generate_challenge(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# Шифрування виклику
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + ciphertext + tag).decode('utf-8')


# Дешифрування виклику
def decrypt_data(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data)
    nonce = encrypted_data[:16]
    ciphertext = encrypted_data[16:-16]
    tag = encrypted_data[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')


# Перевірка відповіді користувача
def check_user_response(user_response, original_challenge):
    return user_response == original_challenge


# Функція для очищення екрану терміналу
def clear_terminal():
    # Перевірка, чи доступна змінна TERM
    if 'TERM' in os.environ:
        if os.name == 'nt':  # Для Windows
            os.system('cls')
        else:  # Для Linux/Mac
            os.system('clear')
    else:
        print("\n" * 100)  # Альтернатива: Прокрутка терміналу вниз


# Основна логіка
def authentication_system():
    # Генерація та шифрування виклику
    challenge = generate_challenge()
    print(f"Ваш пароль для запам'ятовування: {challenge}")

    key = get_random_bytes(32)  # 256-бітний ключ
    encrypted_challenge = encrypt_data(challenge, key)

    print(f"Зашифрований виклик: {encrypted_challenge}")

    # Чекаємо 5 секунд
    time.sleep(5)

    # Очищення екрану
    clear_terminal()

    # Дешифрування виклику для перевірки
    decrypted_challenge = decrypt_data(encrypted_challenge, key)

    # Введення користувачем відповіді
    user_response = input("Введіть відповідь: ")

    # Перевірка відповіді
    if check_user_response(user_response, decrypted_challenge):
        print("Автентифікація пройдена успішно!")
    else:
        print("Помилка автентифікації. Неправильна відповідь.")


# Виклик системи автентифікації
authentication_system()
