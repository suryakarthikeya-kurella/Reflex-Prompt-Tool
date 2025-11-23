import reflex as rx


class SettingsState(rx.State):
    """State for application settings."""

    api_key: str = rx.LocalStorage("", name="api_key")
    theme_mode: str = rx.LocalStorage("dark", name="theme_mode")
    default_task_type: str = rx.LocalStorage("", name="def_task_type")
    default_tone: str = rx.LocalStorage("Professional", name="def_tone")
    default_format: str = rx.LocalStorage("Markdown", name="def_format")
    default_length: str = rx.LocalStorage("Medium (100-300 words)", name="def_length")

    @rx.event
    def set_api_key(self, value: str):
        self.api_key = value

    @rx.event
    def save_settings(self):
        yield rx.toast(
            "Settings saved successfully!",
            title="Success",
            position="bottom-right",
            style={
                "background-color": "#dcfce7",
                "color": "#166534",
                "border": "1px solid #4ade80",
            },
        )

    @rx.event
    def reset_defaults(self):
        self.default_task_type = ""
        self.default_tone = "Professional"
        self.default_format = "Markdown"
        self.default_length = "Medium (100-300 words)"
        yield rx.toast("Defaults reset", position="bottom-right")