class AnimationSet():
    def __init__(self, name, animations):
        self.name = name
        self.animations = animations
        self.current_animation = { 'name': '', 'frame': 0, 'frames': [], 'timer': None }

    def get_animation(self, name):
        for animation in self.animations:
            if animation.name == name:
                return animation
        return False

    def play_animation(self, name):
        animation = self.get_animation(name)
        if animation:
            self.current_animation = { 'name': name, 'frame': 0, 'frames': animation.frames, 'timer': animation.delay }

    def process_animation(self, name):
        if name != self.current_animation['name']:
            self.play_animation(name)

        if self.current_animation['timer'].is_next_stop_reached():
            self.current_animation['frame'] += 1
            if self.current_animation['frame'] > len(self.current_animation['frames']) - 1:
                self.current_animation['frame'] = 0

            return self.current_animation['frames'][self.current_animation['frame']]
        else:
            return False