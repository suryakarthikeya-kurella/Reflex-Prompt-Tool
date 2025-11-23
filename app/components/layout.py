import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar
from app.components.history_sidebar import history_sidebar
from app.components.shortcuts_modal import shortcuts_modal
from app.states.base import BaseState
import reflex as rx


def layout(content: rx.Component) -> rx.Component:
    """Main layout wrapper."""
    return rx.el.div(
        rx.el.div(
            class_name="hidden",
            on_mount=rx.call_script("""
                document.addEventListener('keydown', function(e) {
                    if ((e.metaKey || e.ctrlKey) && ['k', 'g', 'o', '/'].includes(e.key.toLowerCase())) {
                        e.preventDefault();
                        // We need to trigger the Reflex event manually or map it.
                        // Since mapping complex logic in script is hard without knowing internal IDs,
                        // We will rely on a hidden input or just let the user know via the UI hints.
                        // HOWEVER, for this implementation we will use the window_event_listener component provided by Reflex.
                    }
                });
            """),
        ),
        rx.window_event_listener(
            on_key_down=lambda key, modifiers: BaseState.handle_keyboard(key, modifiers)
        ),
        rx.cond(
            BaseState.is_sidebar_open,
            rx.el.div(
                on_click=BaseState.toggle_sidebar,
                class_name="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm",
            ),
            rx.el.div(),
        ),
        sidebar(),
        history_sidebar(),
        shortcuts_modal(),
        rx.el.div(
            navbar(),
            rx.el.main(
                content,
                class_name="p-6 max-w-7xl mx-auto w-full animate-fade-in",
                id="main-content",
            ),
            class_name="flex-1 flex flex-col min-h-screen md:pl-72 transition-all duration-300 bg-[#08090C]",
        ),
        class_name="min-h-screen font-['Montserrat'] bg-[#08090C] text-gray-100",
    )