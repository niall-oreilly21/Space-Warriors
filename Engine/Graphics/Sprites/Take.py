class Take:
    def __init__(self, active_take, frame_rects, is_infinite = True, repeat_count=0):
        self.__active_take = active_take
        self.__frame_rects = frame_rects
        self.__is_infinite = is_infinite
        self.__repeat_count = repeat_count

    @property
    def active_take(self):
        return self.__active_take

    @property
    def frame_rects(self):
        return self.__frame_rects

    @property
    def is_infinite(self):
        return self.__is_infinite

    @property
    def repeat_count(self):
        return self.__repeat_count