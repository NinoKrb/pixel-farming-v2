import os, glob, pygame
from classes.timer import Timer

class Animation():
    def __init__(self, name, path, options, size, margin=0, delay=200):
        super().__init__()
        self.name = name
        self.filenames, self.count = self.get_options(path, name, options)
        self.path = os.path.join(path, name)
        self.size = size
        self.margin = margin
        self.delay = Timer(delay)

        # Base Character Loading
        self.animation_lib_base = self.get_animation_lib(self.path, self.filenames['base'])
        self.base_frames = self.process_frames(self.animation_lib_base, self.margin, self.size, self.count)

        # Haircut Loading
        self.animation_lib_hair = self.get_animation_lib(self.path, self.filenames['haircut'])
        self.haircut_frames = self.process_frames(self.animation_lib_hair, self.margin, self.size, self.count)

        # Tools Loading
        self.animation_lib_tool = self.get_animation_lib(self.path, self.filenames['tools'])
        self.tool_frames = self.process_frames(self.animation_lib_tool, self.margin, self.size, self.count)

        # Merge Images together
        self.frames = self.merge_frames(self.size, self.base_frames, self.haircut_frames, self.tool_frames)

    def get_animation_lib(self, path, filename):
        return pygame.image.load(os.path.join(path, filename))

    def process_frames(self, lib, margin, size, count):
        subsurfaces = []
        margin_offset = 0
        for i in range(count):
            margin_offset += margin
            subsurfaces.append(pygame.Surface.subsurface(lib, (margin_offset + (i * size[0]), 0, size[0], size[1])))
            margin_offset += margin

        return subsurfaces

    def merge_frames(self, size, frames_base, frames_hair, frames_tool):
        merged_frames = []
        for index in range(len(frames_base)):
            merged_frame = pygame.Surface(size, pygame.SRCALPHA)
            merged_frame.blit(frames_base[index], (0,0))
            merged_frame.blit(frames_hair[index], (0,0))
            merged_frame.blit(frames_tool[index], (0,0))
            merged_frames.append(merged_frame)
        return merged_frames

    def get_options(self, path, name, options):
        animation_libs = glob.glob(os.path.join(path, name, "*.png"))
        filenames = {}
        count = 0

        for lib in animation_libs:
            lib = lib.split('/')[-1]
            if options['base'] in lib or options['haircut'] in lib or options['tools'] in lib:
                filename = lib.split('.')[0]
                count = int(filename.split('strip')[-1])

                if options['base'] in lib:
                    filenames['base'] = lib
                elif options['haircut'] in lib:
                    filenames['haircut'] = lib
                elif options['tools'] in lib:
                    filenames['tools'] = lib

        return filenames, count
