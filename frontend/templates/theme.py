from contextlib import contextmanager
from nicegui import ui
from templates.fonts import fonts
from templates.components import menu


@contextmanager
def frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.add_body_html(f'{fonts}')
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')
    ui.add_body_html('<style>body, html { overflow: hidden; }</style>')

    ui.colors(primary='#155e75', secondary='#475569',accent='#facc15',)
    with ui.column().classes('absolute-center items-center h-screen no-wrap p-9 w-full'):
        yield
        
    with ui.header().classes('row items-center justify-center'):
        ui.label('MyVault').classes('lobster-two-bold text-xl')
        
            

    with ui.footer().classes('row items-center justify-center'):
        ui.icon.default_classes('text-2xl pr-2')
        ui.icon('eva-github')
        ui.icon('eva-linkedin-outline')
        ui.icon('eva-twitter')
        

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        pass