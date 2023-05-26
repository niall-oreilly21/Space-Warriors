class Take:
    def __init__(self, active_take, frame_rects):
        self.__active_take = active_take
        self.__frame_rects = frame_rects

    @property
    def active_take(self):
        return self.__active_take

    @property
    def frame_rects(self):
        return self.__frame_rects