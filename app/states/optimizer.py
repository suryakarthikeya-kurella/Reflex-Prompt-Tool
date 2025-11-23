import reflex as rx
import asyncio
import random
import logging


class OptimizerState(rx.State):
    """State for the prompt optimizer page."""

    original_prompt: str = ""
    optimized_prompt: str = ""
    optimization_level: str = "Moderate"
    selected_goals: list[str] = ["Clarity", "Structure"]
    is_optimizing: bool = False
    explanation: list[str] = []
    clarity_score: int = 0
    conciseness_score: int = 0
    structure_score: int = 0
    depth_score: int = 0
    overall_score: int = 0
    goal_options: list[str] = ["Clarity", "Conciseness", "Structure", "Depth"]
    level_options: list[str] = ["Light", "Moderate", "Aggressive"]

    @rx.event
    def set_original_prompt(self, value: str):
        self.original_prompt = value

    @rx.event
    def set_optimization_level(self, value: str):
        self.optimization_level = value

    @rx.event
    def toggle_goal(self, goal: str, checked: bool):
        if checked:
            if goal not in self.selected_goals:
                self.selected_goals.append(goal)
        elif goal in self.selected_goals:
            self.selected_goals.remove(goal)

    @rx.event
    def clear_form(self):
        self.original_prompt = ""
        self.optimized_prompt = ""
        self.explanation = []
        self.clarity_score = 0
        self.conciseness_score = 0
        self.structure_score = 0
        self.depth_score = 0
        self.overall_score = 0

    @rx.event
    async def optimize_prompt(self):
        """Simulate the optimization process."""
        if not self.original_prompt:
            yield rx.toast(
                "Please enter a prompt to optimize.",
                title="Validation Error",
                position="bottom-right",
                style={
                    "background-color": "#fee2e2",
                    "color": "#991b1b",
                    "border": "1px solid #f87171",
                },
            )
            return
        self.is_optimizing = True
        self.optimized_prompt = ""
        yield
        await asyncio.sleep(1.5)
        prefix = ""
        suffix = ""
        changes = []
        if self.optimization_level == "Light":
            prefix = "[Refined] "
            changes.append("Corrected minor grammatical inconsistencies.")
        elif self.optimization_level == "Moderate":
            prefix = "[Optimized] "
            suffix = """

Ensure the output strictly follows these guidelines."""
            changes.append("Enhanced vocabulary for better precision.")
            changes.append("Clarified instruction intent.")
        else:
            prefix = "[Expert-Level Rewrite] "
            suffix = """

Step-by-step reasoning is required before the final answer."""
            changes.append("Completely restructured for maximum logical flow.")
            changes.append("Added strict constraints to prevent hallucinations.")
        modified_body = self.original_prompt
        if "Clarity" in self.selected_goals:
            changes.append("Removed ambiguous terms to improve clarity.")
        if "Conciseness" in self.selected_goals:
            changes.append("Reduced word count by removing redundancy.")
        if "Structure" in self.selected_goals:
            modified_body = f"# Context\n{modified_body}\n\n# Instructions\n- Follow the guidelines below..."
            changes.append("Applied markdown formatting for better structure.")
        if "Depth" in self.selected_goals:
            changes.append("Expanded context requirements for deeper analysis.")
        self.optimized_prompt = f"{prefix}\n{modified_body}{suffix}"
        self.explanation = changes
        self.score_prompt()
        from app.states.history import HistoryState

        hist = await self.get_state(HistoryState)
        preview = (
            self.original_prompt[:30] + "..."
            if len(self.original_prompt) > 30
            else self.original_prompt
        )
        hist.add_item(
            type="optimized",
            title=f"Optimized: {preview}",
            content=self.optimized_prompt,
            metadata={
                "original_prompt": self.original_prompt,
                "optimization_level": self.optimization_level,
                "selected_goals": ",".join(self.selected_goals),
                "explanation": "|".join(self.explanation),
                "scores": f"{self.clarity_score},{self.conciseness_score},{self.structure_score},{self.depth_score}",
            },
        )
        self.is_optimizing = False
        yield rx.toast(
            "Prompt optimized successfully!",
            title="Success",
            position="bottom-right",
            style={
                "background-color": "#dcfce7",
                "color": "#166534",
                "border": "1px solid #4ade80",
            },
        )

    @rx.event
    def score_prompt(self):
        """Generate mock scores."""
        base = 70 if self.optimization_level == "Light" else 80
        if self.optimization_level == "Aggressive":
            base = 85
        self.clarity_score = min(100, base + random.randint(5, 15))
        self.conciseness_score = min(100, base + random.randint(-5, 10))
        self.structure_score = min(100, base + random.randint(0, 15))
        self.depth_score = min(100, base + random.randint(-5, 15))
        self.overall_score = int(
            (
                self.clarity_score
                + self.conciseness_score
                + self.structure_score
                + self.depth_score
            )
            / 4
        )

    @rx.event
    def copy_result(self):
        """Copy the optimized prompt to clipboard."""
        yield rx.set_clipboard(self.optimized_prompt)
        yield rx.toast(
            "Copied to clipboard!",
            position="bottom-right",
            style={
                "background-color": "#dcfce7",
                "color": "#166534",
                "border": "1px solid #4ade80",
            },
        )

    @rx.event
    async def load_from_history(self, metadata: dict, content: str):
        """Load an optimized prompt from history."""
        self.original_prompt = metadata.get("original_prompt", "")
        self.optimization_level = metadata.get("optimization_level", "Moderate")
        self.optimized_prompt = content
        goals_str = metadata.get("selected_goals", "")
        self.selected_goals = goals_str.split(",") if goals_str else []
        expl_str = metadata.get("explanation", "")
        self.explanation = expl_str.split("|") if expl_str else []
        scores_str = metadata.get("scores", "0,0,0,0")
        try:
            c, co, s, d = map(int, scores_str.split(","))
            self.clarity_score = c
            self.conciseness_score = co
            self.structure_score = s
            self.depth_score = d
            self.overall_score = int((c + co + s + d) / 4)
        except Exception as e:
            logging.exception(f"Error parsing scores from history: {e}")
        from app.states.base import BaseState

        base = await self.get_state(BaseState)
        base.show_history = False
        yield rx.redirect("/optimizer")
        yield rx.toast("Restored optimization from history", position="bottom-right")