import glm
from shigg.default_drawing import draw_button, draw_slider, draw_draggable
from shigg.elements import Button, Slider, Draggable

default_draw_kit = {
    "Button": draw_button,
    "Slider": draw_slider,
    "Draggable": draw_draggable,
}


class Gui:
    def __init__(self) -> None:
        self.elements = []
        self.events = []
        self.draw_kit = default_draw_kit

    def add_element(self, element):
        """Add an element to the gui."""
        self.elements.append(element)

    def step(
        self,
        mouse_position: glm.vec2,
        mouse_pressed: bool,
        click=False,
    ):
        """Step the gui, and all elements within it.
        Mouse position should be normalized to the resolution of the gui.
        [0.0, 1.0] if its inside the gui, and [-inf, inf] if its outside.
        """
        for element in self.elements:
            if event := element.step(mouse_position, mouse_pressed):
                self.events.append(event)

    def get_events(self):
        """Get all events that occured since the last call to step.
        Calling this function will clear the event list."""
        events = self.events
        self.events = []
        return events

    def set_draw_kit(self, draw_kit):
        """Set the draw kit for all elements in the gui.
        The draw kit is a dictionary mapping element types to draw functions.
        """
        self.draw_kit = draw_kit

    def draw(self, surface, resolution):
        """Draw the gui to the given surface."""
        # sort elements by type
        self.elements.sort(key=lambda element: element.__class__.__name__)
        for element in self.elements:
            self.draw_kit[element.__class__.__name__](surface, element, resolution)
