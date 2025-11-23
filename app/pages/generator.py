import reflex as rx
from app.components.layout import layout
from app.components.skeleton import loading_card
from app.states.generator import GeneratorState


def preset_button(label: str, tooltip: str) -> rx.Component:
    active = GeneratorState.active_preset == label
    return rx.el.div(
        rx.el.button(
            label,
            on_click=lambda: GeneratorState.set_preset(label),
            class_name=rx.cond(
                active,
                "w-full py-2 rounded-lg bg-teal-900/30 border border-teal-500 text-teal-400 text-sm font-semibold transition-all shadow-[0_0_15px_rgba(45,212,191,0.1)]",
                "w-full py-2 rounded-lg bg-[#1A1D24] border border-gray-800 text-gray-400 text-sm font-medium hover:bg-[#22262E] hover:text-gray-300 transition-all",
            ),
            title=tooltip,
        ),
        class_name="flex-1",
    )


def purpose_item(purpose: str) -> rx.Component:
    active = GeneratorState.purpose == purpose
    return rx.el.button(
        rx.icon(
            GeneratorState.purpose_icons[purpose],
            class_name=rx.cond(
                active,
                "w-5 h-5 text-teal-400 mb-1",
                "w-5 h-5 text-gray-500 mb-1 group-hover:text-gray-400",
            ),
        ),
        rx.el.span(
            purpose,
            class_name=rx.cond(
                active,
                "text-[10px] font-bold text-white leading-tight",
                "text-[10px] font-medium text-gray-400 leading-tight group-hover:text-gray-300",
            ),
        ),
        on_click=lambda: GeneratorState.select_purpose(purpose),
        class_name=rx.cond(
            active,
            "flex flex-col items-center justify-center p-2.5 rounded-lg bg-teal-900/20 border border-teal-500/50 transition-all shadow-md",
            "flex flex-col items-center justify-center p-2.5 rounded-lg bg-[#1A1D24] border border-gray-800 hover:bg-[#22262E] hover:border-gray-700 transition-all group",
        ),
    )


def tone_pill(tone: str) -> rx.Component:
    active = GeneratorState.tone == tone
    return rx.el.button(
        tone,
        on_click=lambda: GeneratorState.set_tone_preset(tone),
        class_name=rx.cond(
            active,
            "px-3 py-1.5 rounded-full bg-teal-900/20 border border-teal-500/50 text-teal-400 text-xs font-bold transition-all",
            "px-3 py-1.5 rounded-full bg-[#1A1D24] border border-gray-800 text-gray-400 text-xs font-medium hover:border-gray-700 hover:text-gray-300 transition-all",
        ),
    )


def example_pill(text: str) -> rx.Component:
    return rx.el.button(
        rx.el.span("+", class_name="text-teal-500 mr-1.5 font-bold"),
        rx.el.span(text, class_name="truncate max-w-[180px]"),
        on_click=lambda: GeneratorState.use_quick_example(text),
        class_name="flex items-center px-3 py-1.5 rounded-full bg-[#1A1D24] border border-gray-800 hover:border-teal-500/30 hover:bg-[#22262E] text-xs text-gray-400 hover:text-gray-200 transition-all whitespace-nowrap",
        title="Click to use this example",
    )


def advanced_accordion() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.span(
                "Advanced Options",
                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider group-hover:text-gray-400",
            ),
            rx.icon(
                "chevron-down",
                class_name=rx.cond(
                    GeneratorState.show_advanced,
                    "w-4 h-4 text-gray-500 transform rotate-180 transition-transform",
                    "w-4 h-4 text-gray-500 transition-transform",
                ),
            ),
            on_click=GeneratorState.toggle_advanced,
            class_name="flex items-center justify-between w-full py-2 border-t border-gray-800 mt-2 mb-2 group hover:bg-white/5 px-2 rounded-lg transition-colors",
        ),
        rx.cond(
            GeneratorState.show_advanced,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Format",
                            class_name="block text-xs text-gray-500 font-medium mb-1.5",
                        ),
                        rx.el.select(
                            rx.foreach(
                                GeneratorState.formats,
                                lambda f: rx.el.option(f, value=f),
                            ),
                            value=GeneratorState.format,
                            on_change=GeneratorState.set_format,
                            class_name="w-full bg-[#13151A] border border-gray-800 rounded-lg px-3 py-2 text-sm text-white focus:border-teal-500 outline-none",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Length",
                            class_name="block text-xs text-gray-500 font-medium mb-1.5",
                        ),
                        rx.el.select(
                            rx.foreach(
                                GeneratorState.lengths,
                                lambda l: rx.el.option(l, value=l),
                            ),
                            value=GeneratorState.length,
                            on_change=GeneratorState.set_length,
                            class_name="w-full bg-[#13151A] border border-gray-800 rounded-lg px-3 py-2 text-sm text-white focus:border-teal-500 outline-none",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Constraints (Optional)",
                        class_name="block text-xs text-gray-500 font-medium mb-1.5",
                    ),
                    rx.el.textarea(
                        placeholder="e.g. No markdown, strict tone...",
                        on_change=GeneratorState.set_constraints,
                        class_name="w-full bg-[#13151A] border border-gray-800 rounded-lg px-3 py-2 text-sm text-white focus:border-teal-500 outline-none min-h-[80px]",
                        default_value=GeneratorState.constraints,
                    ),
                    class_name="mb-4",
                ),
                class_name="p-4 bg-[#1A1D24] rounded-xl border border-gray-800 animate-fade-in",
            ),
        ),
    )


def generator_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Create a Prompt — Fast",
                    class_name="text-3xl md:text-4xl font-bold text-white mb-2 tracking-tight",
                ),
                rx.el.p(
                    "Choose a purpose, describe your need, hit Generate.",
                    class_name="text-base text-gray-400",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        preset_button("Quick", "Minimal instructions"),
                        preset_button("Balanced", "Standard detail"),
                        preset_button("Precise", "Detailed with constraints"),
                        class_name="flex gap-2 mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Purpose",
                            class_name="block text-sm font-bold text-gray-300 mb-3",
                        ),
                        rx.el.div(
                            rx.foreach(GeneratorState.purposes, purpose_item),
                            class_name="grid grid-cols-4 gap-2 mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Describe your need",
                            class_name="block text-sm font-bold text-gray-300 mb-2",
                        ),
                        rx.el.textarea(
                            placeholder="e.g. convert CSV to JSON without pandas",
                            on_change=GeneratorState.set_describe,
                            class_name="w-full bg-[#1A1D24] border border-gray-800 rounded-xl px-4 py-4 text-white text-lg placeholder-gray-600 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500 transition-all resize-none shadow-sm min-h-[120px]",
                            default_value=GeneratorState.describe,
                        ),
                        rx.el.div(
                            rx.el.span(
                                "What do you want the model to do? One sentence is best.",
                                class_name="text-xs text-gray-500",
                            ),
                            rx.cond(
                                (GeneratorState.describe.length() > 0)
                                & (GeneratorState.describe.split(" ").length() < 5),
                                rx.el.span(
                                    " — Try adding more details like expected output.",
                                    class_name="text-xs text-teal-500 font-medium",
                                ),
                            ),
                            class_name="mt-2 mb-3 flex items-center flex-wrap",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Try:",
                                class_name="text-xs font-bold text-gray-500 mr-2",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    GeneratorState.current_purpose_examples,
                                    example_pill,
                                ),
                                class_name="flex gap-2 overflow-x-auto no-scrollbar py-1",
                            ),
                            class_name="flex items-center overflow-hidden mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Tone",
                            class_name="block text-sm font-bold text-gray-300 mb-3",
                        ),
                        rx.el.div(
                            rx.foreach(GeneratorState.tone_presets, tone_pill),
                            class_name="flex flex-wrap gap-2",
                        ),
                        class_name="mb-4",
                    ),
                    advanced_accordion(),
                    rx.el.button(
                        rx.cond(
                            GeneratorState.is_generating,
                            rx.el.span(
                                rx.icon(
                                    "loader",
                                    class_name="animate-spin w-5 h-5 mr-2 inline",
                                ),
                                "Generating...",
                            ),
                            "Generate Prompt",
                        ),
                        on_click=GeneratorState.compose_prompt,
                        disabled=GeneratorState.is_generating,
                        class_name="hidden md:flex w-full bg-teal-600 hover:bg-teal-500 text-white font-bold rounded-xl py-4 items-center justify-center shadow-lg shadow-teal-900/20 transition-all active:scale-[0.99] disabled:opacity-70 disabled:cursor-not-allowed mt-4",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Generated Result",
                                class_name="text-sm font-bold text-gray-400 uppercase tracking-wider",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("disc_2", class_name="w-4 h-4"),
                                    "Optimize",
                                    on_click=GeneratorState.send_to_optimizer,
                                    disabled=GeneratorState.generated_prompt == "",
                                    class_name="text-xs font-medium text-gray-400 hover:text-white flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-800 transition-all disabled:opacity-0",
                                ),
                                rx.el.button(
                                    rx.icon("copy", class_name="w-4 h-4"),
                                    "Copy",
                                    on_click=GeneratorState.copy_to_clipboard,
                                    disabled=GeneratorState.generated_prompt == "",
                                    class_name="text-xs font-medium text-teal-400 hover:text-teal-300 flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-teal-900/20 transition-all ml-2 disabled:opacity-0",
                                ),
                                class_name="flex items-center",
                            ),
                            class_name="flex items-center justify-between mb-4",
                        ),
                        rx.cond(
                            GeneratorState.is_generating,
                            rx.el.div(loading_card(), class_name="opacity-50"),
                            rx.cond(
                                GeneratorState.generated_prompt,
                                rx.el.div(
                                    rx.el.pre(
                                        GeneratorState.generated_prompt,
                                        class_name="text-gray-300 whitespace-pre-wrap font-mono text-sm leading-relaxed",
                                    ),
                                    class_name="min-h-[400px] max-h-[700px] overflow-y-auto custom-scrollbar",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "sparkles",
                                        class_name="w-12 h-12 text-gray-800 mb-4",
                                    ),
                                    rx.el.p(
                                        "No prompt yet — write one line and hit Generate.",
                                        class_name="text-gray-500 text-center max-w-[200px] leading-relaxed",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-[400px] border-2 border-dashed border-gray-800/50 rounded-xl bg-[#13151A]/30",
                                ),
                            ),
                        ),
                        class_name="bg-[#13151A] border border-gray-800 rounded-2xl p-6 shadow-xl h-full min-h-[500px]",
                    ),
                    class_name="sticky top-24",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-[1.2fr_1fr] gap-12 items-start",
            ),
            rx.el.button(
                rx.cond(
                    GeneratorState.is_generating,
                    rx.icon("loader", class_name="animate-spin w-6 h-6"),
                    rx.icon("sparkles", class_name="w-6 h-6"),
                ),
                on_click=GeneratorState.compose_prompt,
                disabled=GeneratorState.is_generating,
                class_name="fixed bottom-6 right-6 md:hidden z-50 p-4 rounded-full bg-teal-600 text-white shadow-2xl shadow-teal-900/50 border border-teal-400/20 active:scale-90 transition-transform disabled:opacity-70",
            ),
        )
    )