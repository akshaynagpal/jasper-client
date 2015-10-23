# -*- coding: utf-8-*-
import abc
import gettext
import jasperpath
import vocabcompiler


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


class STTPlugin(GenericPlugin):
    def __init__(self, name, phrases, *args, **kwargs):
        GenericPlugin.__init__(self, *args, **kwargs)
        self._vocabulary_phrases = phrases
        self._vocabulary_name = name
        self._vocabulary_compiled = False
        self._vocabulary_path = None

    def compile_vocabulary(self, compilation_func):
        if self._vocabulary_compiled:
            raise RuntimeError("Vocabulary has already been compiled!")

        vocabulary = vocabcompiler.VocabularyCompiler(
            self.info.name, self._vocabulary_name,
            path=jasperpath.config('vocabularies'))

        if not vocabulary.matches_phrases(self._vocabulary_phrases):
            vocabulary.compile(
                self.profile, compilation_func, self._vocabulary_phrases)

        self._vocabulary_path = vocabulary.path
        return self._vocabulary_path

    @property
    def vocabulary_path(self):
        return self._vocabulary_path

    @classmethod
    @abc.abstractmethod
    def is_available(cls):
        return True

    @abc.abstractmethod
    def transcribe(self, fp):
        pass
