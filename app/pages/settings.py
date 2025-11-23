import reflex as rx
from app.components.layout import layout
from app.components.layout import layout
from app.states.settings import SettingsState
from app.states.generator import GeneratorState


def setting_section(
    title: str, description: str, content: rx.Component
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(title, class_name="text-lg font-semibold text-white mb-1"),
            rx.el.p(description, class_name="text-sm text-gray-400"),
            class_name="mb-4 md:mb-0 md:w-1/3",
        ),
        rx.el.div(
            content,
            class_name="md:w-2/3 p-6 bg-[#13151A] border border-gray-800 rounded-2xl",
        ),
        class_name="flex flex-col md:flex-row md:gap-8 py-8 border-b border-gray-800 last:border-0",
    )


def settings_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Settings", class_name="text-3xl font-bold text-white mb-2"),
                rx.el.p(
                    "Manage your preferences, defaults, and API configuration.",
                    class_name="text-gray-400",
                ),
                class_name="mb-8",
            ),
            setting_section(
                "API Configuration",
                "Configure external LLM providers for enhanced generation capabilities.",
                rx.el.div(
                    rx.el.label(
                        "OpenAI API Key (Optional)",
                        class_name="block text-sm font-medium text-gray-400 mb-2",
                    ),
                    rx.el.input(
                        type="password",
                        on_change=SettingsState.set_api_key,
                        placeholder="sk-...",
                        class_name="w-full bg-[#1A1D24] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500 outline-none transition-all mb-2",
                        default_value=SettingsState.api_key,
                    ),
                    rx.el.p(
                        "Your key is stored locally in your browser and never sent to our servers.",
                        class_name="text-xs text-gray-500",
                    ),
                ),
            ),
            setting_section(
                "Generator Defaults",
                "Set your preferred starting values for the prompt generator.",
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Default Tone",
                            class_name="block text-sm font-medium text-gray-400 mb-2",
                        ),
                        rx.el.select(
                            rx.foreach(
                                GeneratorState.tones, lambda t: rx.el.option(t, value=t)
                            ),
                            value=SettingsState.default_tone,
                            on_change=SettingsState.set_default_tone,
                            class_name="w-full bg-[#1A1D24] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:border-teal-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Default Format",
                            class_name="block text-sm font-medium text-gray-400 mb-2",
                        ),
                        rx.el.select(
                            rx.foreach(
                                GeneratorState.formats,
                                lambda f: rx.el.option(f, value=f),
                            ),
                            value=SettingsState.default_format,
                            on_change=SettingsState.set_default_format,
                            class_name="w-full bg-[#1A1D24] border border-gray-800 rounded-xl px-4 py-2.5 text-white focus:border-teal-500 outline-none",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.button(
                        "Reset to Defaults",
                        on_click=SettingsState.reset_defaults,
                        class_name="text-sm text-teal-500 hover:text-teal-400 font-medium",
                    ),
                ),
            ),
            setting_section(
                "Appearance",
                "Customize the look and feel of the application.",
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Theme Mode", class_name="text-sm font-medium text-white"
                        ),
                        rx.el.select(
                            rx.el.option("Dark Mode", value="dark"),
                            rx.el.option("Light Mode", value="light"),
                            value=SettingsState.theme_mode,
                            on_change=SettingsState.set_theme_mode,
                            class_name="bg-[#1A1D24] border border-gray-800 rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:border-teal-500 outline-none ml-auto",
                        ),
                        class_name="flex items-center justify-between p-3 rounded-lg bg-[#1A1D24]/50 border border-gray-800/50",
                    )
                ),
            ),
            rx.el.div(
                rx.el.button(
                    "Save Changes",
                    on_click=SettingsState.save_settings,
                    class_name="px-6 py-2.5 bg-teal-600 hover:bg-teal-500 text-white font-semibold rounded-xl transition-all shadow-lg shadow-teal-900/20",
                ),
                class_name="flex justify-end mt-8",
            ),
        )
    )