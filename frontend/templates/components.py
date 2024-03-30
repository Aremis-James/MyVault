from nicegui import ui


class LoginInput(ui.input):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None


class EmailInput(ui.input):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


class DomainSelection(ui.select):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


class LoginButton(ui.button):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

def menu() -> None:
    ui.link.default_classes(replace='text-white')
    ui.link('Home', '/')
    ui.link('Vault', '/youtube-title-generator/')
    ui.link('Password Generator', '/youtube-script/')


if __name__ in {"__main__", "__mp_main__"}:
    pass
    ui.run(window_size=(600,800))