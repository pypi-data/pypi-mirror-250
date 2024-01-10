import reflex as rx

from flexdown import types
from flexdown.blocks.block import Block


demo_box_style = {
    "border_radius": "8px;",
    "border": "2px solid #F4F3F6",
    "box_shadow": "rgba(99, 99, 99, 0.1) 0px 2px 8px 0px;",
    "padding": 5,
    "width": "100%",
    "overflow_x": "auto",
}


class DemoBlock(Block):
    """A block that displays a component along with its code."""

    starting_indicator = "```python demo"
    ending_indicator = "```"
    include_indicators = True

    def render(self, env: types.Env) -> rx.Component:
        content = self.get_content(env)
        code = (
            content.lstrip(self.starting_indicator)
            .rstrip(self.ending_indicator)
            .strip()
        )
        comp = eval(code, env, env)

        return rx.vstack(
            rx.center(comp, style=demo_box_style),
            rx.box(
                rx.markdown(content, component_map=self.component_map),
                width="100%",
            ),
            padding_y="1em",
            spacing="1em",
        )
