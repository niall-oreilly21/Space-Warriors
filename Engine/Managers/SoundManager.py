import pygame.mixer

from Engine.Managers.Manager import Manager
from Engine.Other.Enums.EventEnums import EventCategoryType, EventActionType


class SoundManager(Manager):
    def __init__(self, event_dispatcher):
        super().__init__(event_dispatcher)
        pygame.mixer.init()
        self.__sounds = {}

    def _subscribe_to_events(self):
        self._event_dispatcher.add_listener(EventCategoryType.SoundManager, self._handle_events)

    def _handle_events(self, event_data):
        if event_data.event_action_type == EventActionType.PlaySound:

            sound_name = event_data.parameters[0]
            self.play_sound(sound_name)

        elif event_data.event_action_type == EventActionType.StopSound:
            sound_name = event_data.parameters[0]
            self.stop_sound(sound_name)

        elif event_data.event_action_type == EventActionType.StopAllSounds:
            self.stop_all_sounds()

        elif event_data.event_action_type == EventActionType.SetSoundVolume:
            sound_name = event_data.parameters[0]
            sound_volume = event_data.parameters[1]
            self.set_sound_volume(sound_name, sound_volume)

        elif event_data.event_action_type == EventActionType.SetSoundMasterVolume:
            sound_volume = event_data.parameters[0]
            self.set_master_volume(sound_volume)

    def load_sound(self, sound_name, file_path):
        sound = pygame.mixer.Sound(file_path)
        self.__sounds[sound_name] = sound

    def play_sound(self, sound_name):
        if sound_name in self.__sounds:
            self.__sounds[sound_name].play()

    def stop_sound(self, sound_name):
        if sound_name in self.__sounds:
            self.__sounds[sound_name].stop()

    def stop_all_sounds(self):
        pygame.mixer.stop()


    def set_sound_volume(self, sound_name, volume):
        """
               Set the volume for a sound.

               Args:
                   volume (float): The volume value between 0.0 and 1.0.
                       0.0 represents silence, while 1.0 represents maximum volume.
               """
        if sound_name in self.__sounds:
            self.__sounds[sound_name].set_volume(volume)

    def set_master_volume(self, volume):
        for sound_name in self.__sounds:
            self.__sounds[sound_name].set_volume(volume)



