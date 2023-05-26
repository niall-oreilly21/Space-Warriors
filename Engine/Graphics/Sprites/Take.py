class Take:
    def __init__(self, active_take, frame_rects, is_repeated = True):
        self.__active_take = active_take
        self.__frame_rects = frame_rects
        self.__is_repeated = is_repeated

    @property
    def active_take(self):
        return self.__active_take

    @property
    def frame_rects(self):
        return self.__frame_rects

    @property
    def is_repeated(self):
        return self.__is_repeated