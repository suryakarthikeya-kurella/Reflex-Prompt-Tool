import reflex as rx
from app.components.layout import layout
from app.components.skeleton import loading_card
from app.states.optimizer import OptimizerState


def score_bar(label: str, score: int, color: str) -> rx.Component:
    """A progress bar component for scores."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(label, class_name="text-sm font-medium text-gray-400"),
            rx.el.span(f"{score}/100", class_name="text-sm font-bold text-white"),
            class_name="flex justify-between mb-1.5",
        ),
        rx.el.div(
            rx.el.div(
                class_name=f"h-full rounded-full {color} transition-all duration-1000 ease-out",
                style={"width": f"{score}%"},
            ),
            class_name="w-full h-2 bg-gray-800 rounded-full overflow-hidden",
        ),
    )


def checkbox_option(label: str) -> rx.Component:
    """A checkbox option for optimization goals."""
    is_checked = OptimizerState.selected_goals.contains(label)
    return rx.el.label(
        rx.el.input(
            type="checkbox",
            checked=is_checked,
            on_change=lambda checked: OptimizerState.toggle_goal(label, checked),
            class_name="w-4 h-4 rounded border-gray-700 bg-[#1A1D24] text-teal-600 focus:ring-teal-500 focus:ring-offset-0",
        ),
        rx.el.span(label, class_name="ml-2 text-sm text-gray-300"),
        class_name="flex items-center cursor-pointer select-none p-2 rounded-lg hover:bg-[#1A1D24] transition-colors",
    )


def radio_option(label: str) -> rx.Component:
    """A radio option for optimization level."""
    return rx.el.label(
        rx.el.input(
            type="radio",
            name="opt_level",
            value=label,
            checked=OptimizerState.optimization_level == label,
            on_change=lambda _: OptimizerState.set_optimization_level(label),
            class_name="w-4 h-4 border-gray-700 bg-[#1A1D24] text-teal-600 focus:ring-teal-500 focus:ring-offset-0",
        ),
        rx.el.span(label, class_name="ml-2 text-sm text-gray-300"),
        class_name="flex items-center cursor-pointer select-none p-2 rounded-lg hover:bg-[#1A1D24] transition-colors",
    )


def optimizer_page() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Prompt Optimizer", class_name="text-3xl font-bold text-white mb-2"
                ),
                rx.el.p(
                    "Refine and improve your existing prompts using AI analysis.",
                    class_name="text-gray-400",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Original Prompt",
                            class_name="block text-sm font-medium text-gray-400 mb-2",
                        ),
                        rx.el.textarea(
                            placeholder="Paste your prompt here...",
                            on_change=OptimizerState.set_original_prompt,
                            class_name="w-full h-64 bg-[#1A1D24] border border-gray-800 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500 transition-colors resize-none",
                            default_value=OptimizerState.original_prompt,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Optimization Goals",
                                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    OptimizerState.goal_options, checkbox_option
                                ),
                                class_name="grid grid-cols-2 gap-2",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Optimization Level",
                                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3",
                            ),
                            rx.el.div(
                                rx.foreach(OptimizerState.level_options, radio_option),
                                class_name="space-y-1",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Clear",
                            on_click=OptimizerState.clear_form,
                            class_name="px-6 py-3 rounded-xl text-gray-400 hover:text-white hover:bg-[#1A1D24] transition-all font-medium",
                        ),
                        rx.el.button(
                            rx.cond(
                                OptimizerState.is_optimizing,
                                rx.el.span(
                                    rx.icon(
                                        "loader",
                                        class_name="animate-spin mr-2 inline-block w-4 h-4",
                                    ),
                                    "Optimizing...",
                                ),
                                rx.el.span(
                                    rx.icon(
                                        "wand", class_name="mr-2 inline-block w-4 h-4"
                                    ),
                                    "Optimize Prompt",
                                ),
                            ),
                            on_click=OptimizerState.optimize_prompt,
                            disabled=OptimizerState.is_optimizing,
                            class_name="px-6 py-3 rounded-xl bg-teal-600 text-white font-semibold hover:bg-teal-500 transition-all shadow-lg shadow-teal-900/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center",
                        ),
                        class_name="flex items-center justify-end gap-4",
                    ),
                    class_name="bg-[#13151A] border border-gray-800 rounded-2xl p-6 md:p-8 h-fit",
                ),
                rx.el.div(
                    rx.cond(
                        OptimizerState.is_optimizing,
                        loading_card(),
                        rx.cond(
                            OptimizerState.optimized_prompt,
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            "Optimized Result",
                                            class_name="text-sm font-semibold text-gray-400 uppercase tracking-wider",
                                        ),
                                        rx.el.button(
                                            rx.icon("copy", class_name="w-4 h-4"),
                                            "Copy",
                                            on_click=OptimizerState.copy_result,
                                            class_name="text-sm text-teal-400 hover:text-teal-300 flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-teal-900/20 transition-all",
                                        ),
                                        class_name="flex items-center justify-between mb-4",
                                    ),
                                    rx.el.div(
                                        rx.el.pre(
                                            OptimizerState.optimized_prompt,
                                            class_name="text-gray-300 whitespace-pre-wrap font-mono text-sm leading-relaxed",
                                        ),
                                        class_name="bg-[#0F1115] border border-gray-800 rounded-xl p-4 min-h-[200px] overflow-y-auto max-h-[400px] mb-6",
                                    ),
                                    rx.el.div(
                                        rx.el.h3(
                                            "Analysis & Scores",
                                            class_name="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4",
                                        ),
                                        rx.el.div(
                                            rx.el.div(
                                                rx.el.div(
                                                    rx.el.span(
                                                        "Overall Score",
                                                        class_name="text-gray-400 text-xs uppercase tracking-wider",
                                                    ),
                                                    rx.el.span(
                                                        rx.text(
                                                            OptimizerState.overall_score
                                                        ),
                                                        class_name="text-4xl font-bold text-white mt-1",
                                                    ),
                                                    class_name="flex flex-col items-center justify-center p-4 rounded-xl bg-[#1A1D24] border border-gray-800 mb-4 md:mb-0",
                                                ),
                                                rx.el.div(
                                                    score_bar(
                                                        "Clarity",
                                                        OptimizerState.clarity_score,
                                                        "bg-blue-500",
                                                    ),
                                                    score_bar(
                                                        "Conciseness",
                                                        OptimizerState.conciseness_score,
                                                        "bg-green-500",
                                                    ),
                                                    score_bar(
                                                        "Structure",
                                                        OptimizerState.structure_score,
                                                        "bg-purple-500",
                                                    ),
                                                    score_bar(
                                                        "Depth",
                                                        OptimizerState.depth_score,
                                                        "bg-orange-500",
                                                    ),
                                                    class_name="flex-1 space-y-3",
                                                ),
                                                class_name="grid grid-cols-1 md:grid-cols-[120px_1fr] gap-6 mb-6",
                                            )
                                        ),
                                        rx.el.div(
                                            rx.el.h4(
                                                "Key Improvements",
                                                class_name="text-white font-medium mb-3",
                                            ),
                                            rx.el.ul(
                                                rx.foreach(
                                                    OptimizerState.explanation,
                                                    lambda item: rx.el.li(
                                                        rx.icon(
                                                            "check",
                                                            class_name="w-4 h-4 text-teal-500 mr-2 flex-shrink-0 mt-0.5",
                                                        ),
                                                        rx.el.span(
                                                            item,
                                                            class_name="text-gray-400 text-sm",
                                                        ),
                                                        class_name="flex items-start",
                                                    ),
                                                ),
                                                class_name="space-y-2",
                                            ),
                                            class_name="bg-[#1A1D24]/50 rounded-xl p-4 border border-gray-800/50",
                                        ),
                                    ),
                                    class_name="bg-[#13151A] border border-gray-800 rounded-2xl p-6 animate-fade-in",
                                ),
                                class_name="sticky top-24",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "sparkles",
                                    class_name="w-12 h-12 text-gray-700 mb-4",
                                ),
                                rx.el.h3(
                                    "Ready to Optimize",
                                    class_name="text-xl font-semibold text-white mb-2",
                                ),
                                rx.el.p(
                                    "Paste a prompt and select your goals to see the magic happen.",
                                    class_name="text-gray-500 text-center max-w-xs",
                                ),
                                class_name="flex flex-col items-center justify-center h-full min-h-[400px] rounded-2xl bg-[#13151A]/30 border border-gray-800 border-dashed",
                            ),
                        ),
                    )
                ),
                class_name="grid grid-cols-1 lg:grid-cols-[1.2fr_1fr] gap-8",
            ),
        )
    )