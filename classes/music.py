import pygame
from settings import Settings


class MusicPlayer():
    def __init__(self):
        pygame.mixer.init()

        self.muted = False

        self.playlist = []
        self.reset_playlist()

        pygame.mixer.music.load(self.playlist[0])
        self.queue_soundtrack()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.play()

    def reset_playlist(self, queue=False):
        self.playlist = Settings.default_playlist.copy()
        if queue:
            self.queue_soundtrack()

    def queue_soundtrack(self):
        if self.is_queued():
            pygame.mixer.music.queue(self.playlist.pop())

    def is_queued(self):
        return len(self.playlist) > 0

    def toggle_sounds(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)


