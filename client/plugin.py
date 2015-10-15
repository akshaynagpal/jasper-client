# -*- coding: utf-8-*-
import abc
import gettext


class GenericPlugin(object):
    def __init__(self, info, config):
        self._plugin_config = config
        self._plugin_info = info
        #  TODO: use real translations here
        self._plugin_translations = gettext.NullTranslations()

    @property
    def profile(self):
        # FIXME: Remove this in favor of something better
        return self._plugin_config

    @property
    def info(self):
        return self._plugin_info

    def gettext(self, *args, **kwargs):
        return self._plugin_translations.gettext(*args, **kwargs)

    def ngettext(self, *args, **kwargs):
        return self._plugin_translations.ngettext(*args, **kwargs)


class SpeechHandlerPlugin(GenericPlugin):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_phrases(self):
        pass

    @abc.abstractmethod
    def handle(text, mic):
        pass

    @abc.abstractmethod
    def is_valid(text):
        pass

    def get_priority(self):
        return 0
