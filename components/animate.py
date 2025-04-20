"""module that holds the Animation functionality"""

from dataclasses import dataclass, field
from typing import overload

import pygame

from graphics.textures import TVector2, get_surface_hotspot


class AnimationNotFound(KeyError):
    """Error raised when an animation is not found."""


@dataclass
class Animation:
    """Animation class."""

    frames: list = field(repr=False)
    """ The list of frames to cycle through. """
    speed: int
    """ The speed at which to cycle through the frames. """
    repeat: int
    """ The number of times to repeat the animation. -1 for infinite. """
    loop: bool = field(default=False, init=False, repr=False)
    """ Whether the animation should loop. Defaults to False. """
    current_frame: int = field(default=0, init=False, repr=False)
    """ The current frame of the animation. """
    stop: bool = field(default=False, init=False, repr=False)
    """ Whether the animation should stop. """

    def _post_init_(self):
        self.loop = self.repeat == -1

    @property
    def static(self):
        """Whether the animation is static."""
        return self.speed == 0 or len(self.frames) == 1

    def animate(self):
        """Go to the next frame"""
        if self.static:
            return
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def set_current_frame(self, frame: int):
        """Set the current frame"""
        self.current_frame = frame % len(self.frames)

    def draw(self, window, position):
        """Draw frame(s)"""
        hotspot = get_surface_hotspot(self.frames[self.current_frame]) or TVector2(
            (0, 0)
        )
        window.blit(
            self.frames[self.current_frame],
            (position[0] - hotspot.x, position[1] - hotspot.y),
        )


class AnimatatedObject:
    """An object that can be animated."""

    _current_animation: str = ""

    animations: dict[str, Animation]
    stop: bool = False

    def __init__(self, animations: dict[str, Animation] = None):
        self.animations = {} if animations is None else animations
        self.elapsed = 0
        if list(self.animations):
            self.change_animation(0)

    @overload
    def change_animation(self, index: int, *, reset: bool = True):
        """Change the animation by index."""

    @overload
    def change_animation(self, name: str, *, reset: bool = True):
        """Change the animation by name."""

    def change_animation(self, name: int | str, *, reset: bool = True):
        """
        Change the animation.
        """
        if isinstance(name, int):
            name = list(self.animations)[max(min(name, len(self.animations) - 1), 0)]
        self._current_animation = name
        if reset:
            self.current_animation.set_current_frame(0)

    @property
    def empty(self) -> bool:
        """Check if the object is empty."""
        return len(self.animations) == 0

    @property
    def current_animation(self) -> Animation:
        """Get the current animation."""
        try:
            return self.animations[self._current_animation]
        except KeyError:
            if self._current_animation == "":
                raise AnimationNotFound("No animation selected") from None
            raise AnimationNotFound(
                f"Animation '{self._current_animation}' not found"
            ) from None

    def add_animation(self, name: str, animation: Animation):
        """Add/Override an animation.
        if the animation already exists, it will be overridden
        """
        self.animations[name] = animation

    def draw(self, window, deltatime: int, position):
        """Draw the current animation."""
        animation = self.current_animation
        # TODO: move to an update function, update functions take responsibility of such
        if animation.stop or self.stop or animation.static:
            return
        self.elapsed += deltatime
        frames_to_skip = self.elapsed // animation.speed
        self.elapsed -= frames_to_skip * animation.speed
        for _ in range(frames_to_skip):
            animation.animate()
        animation.draw(window, position)


if __name__ == "__main__":
    pygame.init()
    twindow = pygame.display.set_mode((500, 500))
    freddy = AnimatatedObject()
    frames = [
        pygame.image.load(f"textures/characters/freddy/freddy frame  ({i}).png")
        for i in range(1, 11 + 1)
    ]
    freddy.add_animation("freddy", Animation(frames, speed=40, repeat=-1))
    freddy.change_animation("freddy")
    tclock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    FPS = 60
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    FPS += 10
                elif event.key == pygame.K_DOWN:
                    FPS -= 10
                if event.key == pygame.K_RIGHT:
                    FPS = 60
                elif event.key == pygame.K_LEFT:
                    FPS = 120

        twindow.fill((0, 0, 0))
        fps_text = font.render(
            f"PFPS: {FPS}. FPS: {round(tclock.get_fps())}", True, (255, 255, 255)
        )
        twindow.blit(fps_text, (10, 10))
        freddy.draw(twindow, tclock, (250, 250))
        pygame.display.flip()
        tclock.tick(FPS)
