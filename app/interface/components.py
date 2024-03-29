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
    


if __name__ in {"__main__", "__mp_main__"}:
    pass
    ui.run(window_size=(600,800))