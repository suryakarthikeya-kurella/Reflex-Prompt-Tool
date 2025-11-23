import reflex as rx
from app.states.base import BaseState


def navbar() -> rx.Component:
    """Top navigation bar with breadcrumbs and mobile toggle."""
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="w-6 h-6 text-gray-400"),
                on_click=BaseState.toggle_sidebar,
                class_name="md:hidden p-2 -ml-2 mr-2 rounded-lg hover:bg-gray-800 text-gray-400",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("App", class_name="text-gray-500"),
                    rx.icon("chevron-right", class_name="w-4 h-4 text-gray-600"),
                    rx.el.span(
                        BaseState.page_title, class_name="text-gray-200 font-medium"
                    ),
                    class_name="flex items-center gap-2 text-sm",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("history", class_name="w-5 h-5"),
                    on_click=BaseState.toggle_history,
                    class_name="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-full transition-colors",
                    title="View History",
                ),
                rx.el.button(
                    rx.icon("keyboard", class_name="w-5 h-5"),
                    on_click=BaseState.toggle_shortcuts,
                    class_name="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-full transition-colors",
                    title="Keyboard Shortcuts (Cmd+/)",
                ),
                class_name="flex items-center gap-2 ml-auto",
            ),
            class_name="flex items-center h-16 px-6 border-b border-gray-800 bg-[#0F1115]/80 backdrop-blur-md sticky top-0 z-40",
        )
    )