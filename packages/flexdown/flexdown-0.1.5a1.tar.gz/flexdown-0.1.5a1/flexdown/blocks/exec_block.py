import reflex as rx

from flexdown import types
from flexdown.blocks.block import Block


MODULES = "modules"


class ExecBlock(Block):
    """A block of executable Python code."""

    starting_indicator = "```python exec"
    ending_indicator = "```"

    def render(self, env: types.Env) -> rx.Component:
        # Get the content of the block.
        content = self.get_content(env)

        # Execute the code.
        exec(content, env, env)

        # Return an empty fragment.
        return rx.fragment()
