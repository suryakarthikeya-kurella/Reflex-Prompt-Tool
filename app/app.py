import reflex as rx
from app.pages.home import home_page
from app.pages.generator import generator_page
from app.pages.optimizer import optimizer_page
from app.pages.settings import settings_page

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal", radius="large"),
    stylesheets=["/styles.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(home_page, route="/", title="Dashboard | PromptMaster")
app.add_page(generator_page, route="/generator", title="Generator | PromptMaster")
app.add_page(optimizer_page, route="/optimizer", title="Optimizer | PromptMaster")
app.add_page(settings_page, route="/settings", title="Settings | PromptMaster")