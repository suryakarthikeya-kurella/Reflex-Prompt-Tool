import reflex as rx
from app.states.base import BaseState
from app.states.history import HistoryState, HistoryItem
from app.states.generator import GeneratorState
from app.states.optimizer import OptimizerState


def history_item_card(item: HistoryItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    item.type,
                    class_name=rx.cond(
                        item.type == "generated",
                        "text-[10px] uppercase tracking-wider font-bold text-teal-400 bg-teal-900/30 px-2 py-0.5 rounded",
                        "text-[10px] uppercase tracking-wider font-bold text-purple-400 bg-purple-900/30 px-2 py-0.5 rounded",
                    ),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-3.5 h-3.5"),
                    on_click=HistoryState.delete_item(item.id),
                    class_name="text-gray-500 hover:text-red-400 transition-colors p-1",
                ),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.h4(
                item.title,
                class_name="text-sm font-medium text-gray-200 mb-1 line-clamp-2 leading-snug",
            ),
            rx.el.p(item.formatted_date, class_name="text-xs text-gray-600"),
            class_name="flex-1 cursor-pointer",
            on_click=rx.cond(
                item.type == "generated",
                GeneratorState.load_from_history(item.metadata, item.content),
                OptimizerState.load_from_history(item.metadata, item.content),
            ),
        ),
        class_name="p-3 rounded-lg bg-[#1A1D24] border border-gray-800 hover:border-gray-700 transition-all group",
    )


def history_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3("History", class_name="text-lg font-semibold text-white"),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5"),
                    on_click=BaseState.toggle_history,
                    class_name="text-gray-400 hover:text-white transition-colors",
                ),
                class_name="flex items-center justify-between p-4 border-b border-gray-800",
            ),
            rx.el.div(
                rx.cond(
                    HistoryState.has_history,
                    rx.el.div(
                        rx.foreach(HistoryState.recent_history, history_item_card),
                        class_name="space-y-3 p-4 overflow-y-auto flex-1 custom-scrollbar",
                    ),
                    rx.el.div(
                        rx.icon("history", class_name="w-12 h-12 text-gray-800 mb-3"),
                        rx.el.p("No history yet", class_name="text-gray-500 text-sm"),
                        class_name="flex flex-col items-center justify-center h-full text-center p-8",
                    ),
                ),
                class_name="flex-1 overflow-hidden flex flex-col",
            ),
            rx.cond(
                HistoryState.has_history,
                rx.el.div(
                    rx.el.button(
                        "Clear History",
                        on_click=HistoryState.clear_history,
                        class_name="w-full py-2 text-xs text-red-400 hover:text-red-300 hover:bg-red-900/10 rounded-lg transition-colors",
                    ),
                    class_name="p-4 border-t border-gray-800",
                ),
            ),
            class_name="flex flex-col h-full bg-[#0F1115]",
        ),
        class_name=rx.cond(
            BaseState.show_history,
            "fixed inset-y-0 right-0 w-80 bg-[#0F1115] border-l border-gray-800 shadow-2xl transform transition-transform duration-300 z-50",
            "fixed inset-y-0 right-0 w-80 bg-[#0F1115] border-l border-gray-800 shadow-2xl transform transition-transform duration-300 z-50 translate-x-full",
        ),
    )