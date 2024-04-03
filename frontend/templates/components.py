from nicegui import ui


def loginCard():
    pass

def menu() -> None:
    ui.link.default_classes(replace='text-white')
    ui.link('Home', '/')
    ui.link('Vault', '/youtube-title-generator/')
    ui.link('Password Generator', '/youtube-script/')


if __name__ in {"__main__", "__mp_main__"}:
    pass
    ui.run(window_size=(600,800))