import reflex as rx
from app.components.layout import layout


def feature_card(icon: str, title: str, description: str, delay: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="w-6 h-6 text-teal-400"),
            class_name="w-12 h-12 rounded-lg bg-teal-900/20 border border-teal-900/50 flex items-center justify-center mb-4",
        ),
        rx.el.h3(title, class_name="text-lg font-semibold text-white mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-400 leading-relaxed"),
        class_name=f"p-6 rounded-2xl bg-[#13151A] border border-gray-800 hover:border-teal-900/50 hover:shadow-lg hover:shadow-teal-900/10 transition-all duration-300 group {delay}",
    )


def home_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "New Version 2.0",
                        class_name="px-3 py-1 rounded-full bg-teal-900/30 border border-teal-900/50 text-teal-400 text-xs font-semibold mb-6 inline-block",
                    ),
                    rx.el.h1(
                        rx.el.span("Master the Art of "),
                        rx.el.span(
                            "Prompting",
                            class_name="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-teal-200",
                        ),
                        class_name="text-5xl md:text-6xl font-bold tracking-tight text-white mb-6 leading-tight",
                    ),
                    rx.el.p(
                        "Generate, optimize, and manage high-quality AI prompts with our advanced toolkit. Designed for prompt engineers and developers who demand precision.",
                        class_name="text-lg text-gray-400 mb-8 max-w-2xl leading-relaxed",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "Start Generating",
                                rx.icon("arrow-right", class_name="w-4 h-4 ml-2"),
                                class_name="flex items-center px-6 py-3 rounded-xl bg-teal-600 text-white font-semibold hover:bg-teal-500 transition-all shadow-lg shadow-teal-900/20 hover:shadow-teal-900/40",
                            ),
                            href="/generator",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "View Documentation",
                                class_name="px-6 py-3 rounded-xl bg-[#1A1D24] text-gray-300 font-semibold hover:bg-[#22262E] border border-gray-800 hover:border-gray-700 transition-all",
                            ),
                            href="#",
                        ),
                        class_name="flex flex-wrap gap-4",
                    ),
                    class_name="flex flex-col items-start justify-center py-16 md:py-24",
                ),
                class_name="w-full border-b border-gray-800 mb-12",
            ),
            rx.el.div(
                rx.el.h2(
                    "Why choose PromptMaster?",
                    class_name="text-2xl font-bold text-white mb-8",
                ),
                rx.el.div(
                    feature_card(
                        "wand-sparkles",
                        "Smart Generation",
                        "Create detailed prompts from simple ideas using our advanced template engine tailored for LLMs.",
                        "animate-fade-in",
                    ),
                    feature_card(
                        "gauge",
                        "AI Optimization",
                        "Refine your prompts automatically to improve clarity, structure, and token efficiency.",
                        "animate-fade-in [animation-delay:100ms]",
                    ),
                    feature_card(
                        "history",
                        "Version History",
                        "Track changes and manage multiple versions of your prompts without losing context.",
                        "animate-fade-in [animation-delay:200ms]",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="mb-16",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Keyboard Shortcuts",
                        class_name="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Cmd + K",
                                class_name="px-2 py-1 rounded bg-gray-800 text-gray-300 text-xs font-mono border border-gray-700",
                            ),
                            rx.el.span("Search", class_name="text-sm text-gray-500"),
                            class_name="flex items-center justify-between p-3 rounded-lg bg-[#13151A] border border-gray-800",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Cmd + G",
                                class_name="px-2 py-1 rounded bg-gray-800 text-gray-300 text-xs font-mono border border-gray-700",
                            ),
                            rx.el.span(
                                "Quick Generate", class_name="text-sm text-gray-500"
                            ),
                            class_name="flex items-center justify-between p-3 rounded-lg bg-[#13151A] border border-gray-800",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    class_name="p-6 rounded-2xl bg-[#13151A]/50 border border-dashed border-gray-800",
                )
            ),
            class_name="flex flex-col",
        )
    )