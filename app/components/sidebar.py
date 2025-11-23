import reflex as rx
from app.states.base import BaseState, NavItem


def sidebar_item(item: NavItem) -> rx.Component:
    """Render a single sidebar navigation item."""
    active = BaseState.current_path == item.path
    return rx.el.a(
        rx.el.div(
            rx.icon(
                item.icon,
                class_name=rx.cond(
                    active,
                    "w-5 h-5 text-teal-400",
                    "w-5 h-5 text-gray-400 group-hover:text-gray-200",
                ),
            ),
            rx.el.span(item.label, class_name="font-medium text-sm"),
            class_name=rx.cond(
                active,
                "flex items-center gap-3 px-3 py-2.5 rounded-lg bg-teal-900/20 text-teal-400 border border-teal-900/50",
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-400 hover:bg-gray-800/50 hover:text-gray-200 transition-all duration-200 group",
            ),
        ),
        href=item.path,
        on_click=BaseState.close_sidebar,
        class_name="block mb-1",
    )


def sidebar() -> rx.Component:
    """The main sidebar component."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("sparkles", class_name="w-6 h-6 text-teal-500"),
                rx.el.span(
                    "Prompt", class_name="text-xl font-bold text-white tracking-tight"
                ),
                rx.el.span(
                    "Master",
                    class_name="text-xl font-bold text-teal-500 tracking-tight",
                ),
                class_name="flex items-center gap-2 px-2",
            ),
            class_name="h-16 flex items-center border-b border-gray-800 mb-6",
        ),
        rx.el.nav(
            rx.foreach(BaseState.nav_items, sidebar_item),
            class_name="flex-1 overflow-y-auto space-y-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="w-4 h-4 text-gray-400"),
                    class_name="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center border border-gray-700",
                ),
                rx.el.div(
                    rx.el.p("Demo User", class_name="text-sm font-medium text-white"),
                    rx.el.p("Free Plan", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3 p-3 rounded-xl bg-gray-900/50 border border-gray-800",
            ),
            class_name="mt-auto pt-6 border-t border-gray-800",
        ),
        class_name=rx.cond(
            BaseState.is_sidebar_open,
            "fixed inset-y-0 left-0 z-50 w-72 bg-[#0F1115] border-r border-gray-800 p-4 flex flex-col transition-transform duration-300 ease-in-out translate-x-0",
            "fixed inset-y-0 left-0 z-50 w-72 bg-[#0F1115] border-r border-gray-800 p-4 flex flex-col transition-transform duration-300 ease-in-out -translate-x-full md:translate-x-0",
        ),
    )