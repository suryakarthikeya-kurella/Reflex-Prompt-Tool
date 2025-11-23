import reflex as rx
import asyncio
from pydantic import BaseModel


class ExampleTemplate(BaseModel):
    name: str
    purpose: str
    describe: str
    tone: str
    format: str
    length: str
    constraints: str
    examples: str


class GeneratorState(rx.State):
    """State for the prompt generator page."""

    purpose: str = "Code"
    describe: str = ""
    tone: str = "Technical"
    active_preset: str = "Balanced"
    format: str = "Python Script"
    length: str = "Medium (100-300 words)"
    constraints: str = ""
    examples: str = ""
    generated_prompt: str = ""
    is_generating: bool = False
    show_advanced: bool = False
    purposes: list[str] = [
        "Code",
        "Email",
        "Blog",
        "Social Post",
        "Script",
        "Creative",
        "Analysis",
        "Other",
    ]
    purpose_icons: dict[str, str] = {
        "Code": "code",
        "Email": "mail",
        "Blog": "pen-tool",
        "Social Post": "share-2",
        "Script": "file-text",
        "Creative": "feather",
        "Analysis": "bar-chart-2",
        "Other": "more-horizontal",
    }
    tone_presets: list[str] = ["Technical", "Friendly", "Formal"]
    auto_constraints: dict[str, str] = {
        "Code": "Return only code. No conversational filler. Include comments.",
        "Email": "Use professional email structure. Be concise and polite.",
        "Blog": "Engaging and SEO-friendly. Use headings and short paragraphs.",
        "Social Post": "Catchy hook, emojis where appropriate, include hashtags.",
        "Script": "Natural dialogue flow. Include scene directions.",
        "Creative": "Show, don't tell. Vivid imagery and emotional resonance.",
        "Analysis": "Data-driven, objective, bullet points for key insights.",
        "Other": "Clear and direct response.",
    }
    tones: list[str] = [
        "Professional",
        "Casual",
        "Enthusiastic",
        "Authoritative",
        "Empathetic",
        "Humorous",
        "Academic",
        "Persuasive",
        "Technical",
        "Friendly",
        "Formal",
    ]
    formats: list[str] = [
        "Paragraph",
        "Bullet Points",
        "Markdown",
        "HTML Code",
        "JSON",
        "Python Script",
        "Email Format",
        "Essay",
        "Step-by-Step Guide",
        "Code",
        "Script",
        "Social Media Post",
    ]
    lengths: list[str] = [
        "Short (< 100 words)",
        "Medium (100-300 words)",
        "Long (300-1000 words)",
        "Detailed (> 1000 words)",
    ]
    purpose_examples: dict[str, list[str]] = {
        "Code": [
            "Python script to scrape a website",
            "React component for a login form",
            "SQL query for monthly churn",
        ],
        "Email": [
            "Cold outreach to potential client",
            "Follow-up after interview",
            "Out of office reply",
        ],
        "Blog": [
            "Benefits of remote work",
            "Guide to personal finance",
            "Review of iPhone 15",
        ],
        "Social Post": [
            "Launch announcement for new product",
            "Motivational quote for Monday",
            "Poll about AI trends",
        ],
        "Script": [
            "Podcast intro about tech news",
            "YouTube video opener",
            "Sales call script",
        ],
        "Creative": [
            "Sci-fi story about Mars colony",
            "Poem about the ocean",
            "Character description for a hero",
        ],
        "Analysis": [
            "Summarize sales data trends",
            "Compare two marketing strategies",
            "SWOT analysis for a startup",
        ],
        "Other": [
            "Study plan for exams",
            "Birthday party ideas",
            "Explain quantum physics",
        ],
    }

    @rx.var
    def task_type(self) -> str:
        return self.purpose

    @rx.var
    def topic(self) -> str:
        return self.describe

    @rx.var
    def current_purpose_examples(self) -> list[str]:
        return self.purpose_examples.get(self.purpose, [])

    @rx.event
    def toggle_advanced(self):
        self.show_advanced = not self.show_advanced

    @rx.event
    def set_preset(self, preset: str):
        self.active_preset = preset
        base_constraint = self.auto_constraints.get(self.purpose, "")
        if preset == "Quick":
            self.length = "Short (< 100 words)"
            self.constraints = base_constraint
        elif preset == "Balanced":
            self.length = "Medium (100-300 words)"
            self.constraints = base_constraint
        elif preset == "Precise":
            self.length = "Detailed (> 1000 words)"
            extras = (
                "Ensure high accuracy. Cite sources if applicable. No hallucinations."
            )
            if base_constraint:
                self.constraints = f"{base_constraint}\n{extras}"
            else:
                self.constraints = extras

    @rx.event
    def select_purpose(self, purpose: str):
        self.purpose = purpose
        if purpose == "Code":
            self.format = "Code"
            self.tone = "Technical"
        elif purpose == "Email":
            self.format = "Email Format"
            self.tone = "Friendly"
        elif purpose == "Blog":
            self.format = "Markdown"
            self.tone = "Friendly"
        elif purpose == "Social Post":
            self.format = "Social Media Post"
            self.tone = "Enthusiastic"
        elif purpose == "Script":
            self.format = "Script"
            self.tone = "Casual"
        elif purpose == "Creative":
            self.format = "Paragraph"
            self.tone = "Creative"
        elif purpose == "Analysis":
            self.format = "Markdown"
            self.tone = "Analytical"
        elif purpose == "Other":
            self.format = "Paragraph"
            self.tone = "Professional"
        self.set_preset(self.active_preset)

    @rx.event
    def set_tone_preset(self, tone: str):
        self.tone = tone

    @rx.event
    def use_quick_example(self, text: str):
        self.describe = text
        self.compose_prompt()

    @rx.event
    async def send_to_optimizer(self):
        from app.states.optimizer import OptimizerState

        opt_state = await self.get_state(OptimizerState)
        opt_state.original_prompt = self.generated_prompt
        yield rx.redirect("/optimizer")

    @rx.event
    async def compose_prompt(self):
        """Construct the prompt based on form inputs."""
        if not self.purpose or not self.describe:
            yield rx.toast(
                "Please select a purpose and describe what you need.",
                title="Validation Error",
                position="bottom-right",
                style={
                    "background-color": "#fee2e2",
                    "color": "#991b1b",
                    "border": "1px solid #f87171",
                },
            )
            return
        self.is_generating = True
        yield
        await asyncio.sleep(0.8)
        parts = []
        parts.append(f"# Role\nAct as an expert in {self.purpose}.")
        parts.append(f"\n# Task\nTopic: {self.describe}")
        if self.tone:
            parts.append(f"Tone: {self.tone}")
        if self.length:
            parts.append(f"Length: {self.length}")
        if self.format:
            parts.append(f"Output Format: {self.format}")
        if self.constraints:
            parts.append(f"\n# Constraints\n{self.constraints}")
        if self.examples:
            parts.append(f"\n# Examples\n{self.examples}")
        parts.append("""
# Instructions
Please generate the response following the requirements above. Ensure high quality and strict adherence to the constraints.""")
        self.generated_prompt = """
""".join(parts)
        from app.states.history import HistoryState

        hist = await self.get_state(HistoryState)
        hist.add_item(
            type="generated",
            title=f"{self.purpose}: {self.describe}",
            content=self.generated_prompt,
            metadata={
                "task_type": self.purpose,
                "topic": self.describe,
                "tone": self.tone,
                "format": self.format,
                "length": self.length,
                "constraints": self.constraints,
                "examples": self.examples,
            },
        )
        self.is_generating = False
        yield rx.toast(
            "Prompt generated successfully!",
            title="Success",
            position="bottom-right",
            style={
                "background-color": "#dcfce7",
                "color": "#166534",
                "border": "1px solid #4ade80",
            },
        )

    @rx.event
    def load_example(self, example: dict):
        """Load an example template into the form."""
        self.purpose = example.get("purpose", "Code")
        self.describe = example.get("describe", "")
        self.tone = example.get("tone", "Technical")
        self.format = example.get("format", "Python Script")
        self.length = example.get("length", "Medium")
        self.constraints = example.get("constraints", "")
        self.examples = example.get("examples", "")
        return rx.toast(
            f"Loaded template: {example.get('name')}", position="bottom-right"
        )

    @rx.event
    async def load_from_history(self, metadata: dict, content: str):
        """Load a prompt from history."""
        self.purpose = metadata.get("task_type") or metadata.get("purpose", "Code")
        self.describe = metadata.get("topic") or metadata.get("describe", "")
        self.tone = metadata.get("tone", "")
        self.format = metadata.get("format", "")
        self.length = metadata.get("length", "")
        self.constraints = metadata.get("constraints", "")
        self.examples = metadata.get("examples", "")
        self.generated_prompt = content
        from app.states.base import BaseState

        base = await self.get_state(BaseState)
        base.show_history = False
        yield rx.redirect("/generator")
        yield rx.toast("Restored prompt from history", position="bottom-right")

    @rx.event
    def clear_form(self):
        """Reset all form fields."""
        self.purpose = "Code"
        self.describe = ""
        self.tone = "Technical"
        self.format = "Python Script"
        self.length = "Medium (100-300 words)"
        self.constraints = ""
        self.examples = ""
        self.generated_prompt = ""
        self.select_purpose("Code")

    @rx.event
    def copy_to_clipboard(self):
        """Copy the generated prompt to clipboard."""
        yield rx.set_clipboard(self.generated_prompt)
        yield rx.toast(
            "Copied to clipboard!",
            position="bottom-right",
            style={
                "background-color": "#dcfce7",
                "color": "#166534",
                "border": "1px solid #4ade80",
            },
        )