import reflex as rx


class NavItem(rx.Base):
    label: str
    path: str
    icon: str


class BaseState(rx.State):
    """The base state for the application."""

    is_sidebar_open: bool = False
    nav_items: list[NavItem] = [
        NavItem(label="Home", path="/", icon="layout-dashboard"),
        NavItem(label="Generator", path="/generator", icon="wand-sparkles"),
        NavItem(label="Optimizer", path="/optimizer", icon="gauge"),
        NavItem(label="Settings", path="/settings", icon="settings"),
    ]

    @rx.var
    def current_path(self) -> str:
        """Get the current path for active state styling."""
        return self.router.page.path

    @rx.var
    def page_title(self) -> str:
        """Get the current page title based on path."""
        path = self.router.page.path
        if path == "/":
            return "Dashboard"
        return path.strip("/").capitalize()

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar on mobile."""
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def close_sidebar(self):
        """Close the sidebar."""
        self.is_sidebar_open = False

    show_history: bool = False
    show_shortcuts: bool = False

    @rx.event
    def toggle_history(self):
        self.show_history = not self.show_history

    @rx.event
    def toggle_shortcuts(self):
        self.show_shortcuts = not self.show_shortcuts

    @rx.event
    def handle_keyboard(self, key: str, modifiers: list[str]):
        """Handle global keyboard shortcuts."""
        is_cmd = "Meta" in modifiers or "Control" in modifiers
        key = key.lower()
        if is_cmd and key == "k":
            yield rx.toast("Search not implemented yet", icon="search")
        elif is_cmd and key == "g":
            yield rx.redirect("/generator")
        elif is_cmd and key == "o":
            yield rx.redirect("/optimizer")
        elif is_cmd and key == "/":
            self.show_shortcuts = not self.show_shortcuts