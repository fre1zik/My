import re
import random
import string
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Для работы с сессиями, например, для капчи

# Функция для проверки валидности ФИО (только буквы и пробелы)
def is_valid_fio(fio):
    return bool(re.match(r'^[А-Яа-яЁё\s]+$', fio))

# Функция для проверки валидности номера телефона
def is_valid_phone(phone):
    return bool(re.match(r'^\+?\d{10,15}$', phone))  # Допускаем номера длиной от 10 до 15 цифр

# Функция для проверки адреса (минимум 5 символов)
def is_valid_address(address):
    return len(address.strip()) >= 5

# Функция для генерации случайной капчи (4 цифры)
def generate_captcha():
    return ''.join(random.choices(string.digits, k=4))

# Функция для получения IP-адреса пользователя
def get_user_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return request.remote_addr

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    fio = ""
    data = ""
    address = ""
    phone_number = ""
    telegram_username = ""
    captcha_input = ""
    invalid_input = ""

    # Генерация капчи и сохранение в сессии
    captcha = session.get('captcha', generate_captcha())
    session['captcha'] = captcha

    # Логирование IP-адреса пользователя
    user_ip = get_user_ip()
    print(f"Пользователь зашел на сайт с IP-адресом: {user_ip}")

    if request.method == 'POST':
        # Получаем данные из формы
        fio = request.form.get('fio')
        data = request.form.get('data')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')
        telegram_username = request.form.get('telegram_username')
        captcha_input = request.form.get('captcha')

        # Логирование введенных данных
        print(f"Введенные данные: ФИО: {fio}, Телефон: {phone_number}, Адрес: {address}, Telegram: {telegram_username}, Доп. данные: {data}, Капча: {captcha_input}, IP: {user_ip}")

        # Проверка капчи и введенных данных
        if captcha_input != session['captcha']:
            invalid_input = "Капча введена неверно. Попробуйте ещё раз."
        elif not is_valid_fio(fio):
            invalid_input = "Неверное ФИО. Используйте только буквы и пробелы."
        elif not is_valid_phone(phone_number):
            invalid_input = "Неверный номер телефона. Убедитесь, что номер состоит из 10-15 цифр."
        elif not is_valid_address(address):
            invalid_input = "Адрес должен содержать минимум 5 символов."
        elif len(telegram_username.strip()) == 0:
            invalid_input = "Поле Telegram username не должно быть пустым."
        else:
            invalid_input = None  # Все данные валидны
            # Здесь можно добавить обработку успешной отправки формы, например, сохранение данных или перенаправление

    return render_template(
        'index.html',
        fio=fio,
        data=data,
        address=address,
        phone_number=phone_number,
        telegram_username=telegram_username,
        invalid_input=invalid_input,
        captcha=captcha
    )

# Новый маршрут для FAQ
@app.route('/faq')
def faq():
    user_ip = get_user_ip()
    print(f"FAQ посещен пользователем с IP-адресом: {user_ip}")
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
