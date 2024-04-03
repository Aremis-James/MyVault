from re import T
from nicegui import ui
from templates.fonts import fonts
import httpx
from templates.theme import frame

ui.add_head_html(f'{fonts}')

def login(email: str, password:str):
    url = 'http://127.0.0.1:8000/v1/login/token'
    data = {'username': email, 'password': password}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = httpx.post(url, data=data, headers=headers)

    match response.status_code:

        case 202:
            ui.notify('Login successful', type='positive')

        case 422:
            detail = response.json().get('detail', 'Login failed')
            ui.notify(detail, type='negative')
        case _:
            ui.notify('bananas', type='warning')

with frame('Login'):
    with ui.card().classes('mt-60'):
        ui.input.default_classes('')
        email= ui.input('email', on_change=None)
        password = ui.input('password', password=True, password_toggle_button=True, on_change=None)
    ui.button('Login', on_click=lambda: login(email.value, password.value))


ui.run(window_size=(500, 800), dark=True,frameless=True)
