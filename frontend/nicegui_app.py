from re import T
from nicegui import ui
from templates.fonts import fonts
import requests
from templates.theme import frame

ui.add_head_html(f'{fonts}')

def login(email: str, password:str):
    url = 'http://127.0.0.1:8000/user/login'
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        ui.notify('Login successful', type='positive')
    else:
        detail = response.json().get('details', 'Login failed')
        ui.notify(detail, type='negative')

with frame('Login'):
    with ui.card().classes('mt-60'):
        ui.input.default_classes('lobster')
        email = ui.input('email', on_change=None).classes('lobster')
        password = ui.input('password', password=True, password_toggle_button=True, on_change=None)
    # ui.button('Login', on_click=lambda: login(email.value, password.value))


ui.run(window_size=(600, 800), dark=True, frameless=True)
