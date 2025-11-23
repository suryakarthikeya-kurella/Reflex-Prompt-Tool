import reflex as rx
from app.states.base import BaseState


def shortcut_row(keys: list[str], description: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(description, class_name="text-sm text-gray-300"),
        rx.el.div(
            rx.foreach(
                keys,
                lambda k: rx.el.kbd(
                    k,
                    class_name="px-2 py-1 rounded bg-gray-800 border border-gray-700 text-gray-400 text-xs font-mono min-w-[24px] text-center",
                ),
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center justify-between py-2 border-b border-gray-800 last:border-0",
    )


def shortcuts_modal() -> rx.Component:
    return rx.cond(
        BaseState.show_shortcuts,
        rx.el.div(
            rx.el.div(
                class_name="absolute inset-0 bg-black/60 backdrop-blur-sm",
                on_click=BaseState.toggle_shortcuts,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Keyboard Shortcuts",
                        class_name="text-lg font-semibold text-white",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-5 h-5"),
                        on_click=BaseState.toggle_shortcuts,
                        class_name="text-gray-400 hover:text-white",
                    ),
                    class_name="flex items-center justify-between mb-6",
                ),
                rx.el.div(
                    shortcut_row(["Cmd", "K"], "Open Search"),
                    shortcut_row(["Cmd", "G"], "Go to Generator"),
                    shortcut_row(["Cmd", "O"], "Go to Optimizer"),
                    shortcut_row(["Cmd", "/"], "Toggle Help"),
                    class_name="space-y-1",
                ),
                class_name="relative w-full max-w-md bg-[#13151A] border border-gray-800 rounded-2xl p-6 shadow-2xl transform transition-all",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in",
        ),
    )