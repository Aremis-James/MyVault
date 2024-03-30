from typing import Tuple
import ast
import string
from secrets import SystemRandom
# from style import kantumruy

from nicegui import ui
import time
from nicegui.events import ValueChangeEventArguments, KeyEventArguments



class NiceUi:
    def __init__(self) -> None:
        self.setup_theme()
        self.login()
        

    def setup_theme(self):
        ui.query('body').style('background-color: #155e75')
        # ui.add_head_html(f'{kantumruy}')
    

            

    

    @ui.page('/login')
    def login(self):
        self.email = None
        self.password = None
        self.domains = ['@gmail.com', '@yahoo.com', '@outlook.com', '@hotmail.com ']
       
        with ui.grid().classes('w-full justify-center mt-40'):
                with ui.tabs().classes('w-full') as tabs:

                    tabs.props('''
                            active-color="pink-4"
                            indicator-color="pink-4"
                            narrow-indicator class="q-mb-lg"

                            ''')
                    
                    login_tab = ui.tab('Login').classes('kantumruy-pro')


                with ui.tab_panels(tabs).classes('w-full').style(f'background-color:#155e75'):
                    with ui.tab_panel(login_tab):
                        with ui.card().classes('bg-slate-500'):
                            ui.input.default_classes('kantumruy-pro')
                            self.email = ui.input('Email:').props(f'color="pink-4"')
                            with self.email:
                                domain_select =  ui.select(self.domains, value=self.domains[0]).props(f'color="pink-4"').classes('kantumruy-pro')
                            
                            self.password = ui.input('Password:', password=True, password_toggle_button=True).props(f'color="pink-4" size=32').classes('pb-6')

                            login = ui.button('Log In', on_click=lambda : self.try_login(self.email, self.password, domain_select), color='pink-4').classes('self-center')
    
    
    def try_login(self, email_input:ui.input, password_input:ui.input, domain: ui.select ):
        admin = {'username': 'admin@gmail.com', 'password': 'R@spb3rry'}
        if email_input.value + domain.value == admin['username'] and password_input.value == admin['password']:
            ui.notify('Success!', type='positive')
        else:
            ui.notify('Invalid credentials', type='negative')
            self.email.set_value(None)
            self.password.set_value(None)
            

    @ui.page('/home')
    def home(self):
        ui.label('Welcome to the Hub!')

    @ui.page('/settings')
    def settings(self):
        pass

    @ui.page('/settings/theme')
    def theme(self):
        pass

    @ui.page('/generate_password')
    def generate_password(self):
        pass

    def __password_generator(self, characters: Tuple[int,int], digits: Tuple[int,int], punctuation: Tuple[int,int]):
        random = SystemRandom()
        characters = ( 
                random.choices(string.ascii_letters, k=random.randint(*characters)) +
                random.choices(string.digits, k=random.randint(*digits)) +
                random.choices(string.punctuation.replace('.',''), k=random.randint(*punctuation)))
        random.shuffle(characters)
        return ''.join(characters)

    def __password_on_click(self):
        # new_password = self._password_generator()
        pass

    def __validate_value(self, value, min:int, max:int):
        try:
            evaluated_value = ast.literal_eval(value)
            
            if isinstance(evaluated_value, tuple):

                return all(min <= val <= max for val in evaluated_value)
            else:
                return min <= evaluated_value <= max
        except (ValueError, SyntaxError):
                    return False

    @ui.page('/vault')
    def vault(self):
        pass

if __name__ in {"__main__", "__mp_main__"}:
    app = NiceUi()
    ui.run(window_size=(600,800), dark=True)
    