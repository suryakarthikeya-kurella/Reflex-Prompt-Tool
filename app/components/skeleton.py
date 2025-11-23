import reflex as rx


def skeleton(
    height: str = "h-4",
    width: str = "w-full",
    rounded: str = "rounded",
    class_name: str = "",
) -> rx.Component:
    """A loading skeleton component."""
    return rx.el.div(
        class_name=f"animate-pulse bg-gray-800 {height} {width} {rounded} {class_name}"
    )


def loading_card() -> rx.Component:
    """A generic loading card skeleton."""
    return rx.el.div(
        rx.el.div(
            skeleton(height="h-6", width="w-1/3", class_name="mb-4"),
            skeleton(height="h-4", width="w-full", class_name="mb-2"),
            skeleton(height="h-4", width="w-5/6", class_name="mb-2"),
            skeleton(height="h-4", width="w-4/6"),
            class_name="flex-1",
        ),
        class_name="p-6 rounded-2xl bg-[#13151A] border border-gray-800",
    )