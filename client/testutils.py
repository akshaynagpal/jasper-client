# -*- coding: utf-8-*-


class TestMic(object):
    def __init__(self, inputs=[]):
        self.inputs = inputs
        self.idx = 0
        self.outputs = []

    def wait_for_keyword(self, keyword="JASPER"):
        return

    def active_listen(self, timeout=3):
        if self.idx < len(self.inputs):
            self.idx += 1
            return [self.inputs[self.idx - 1]]
        return [""]

    def say(self, phrase):
        self.outputs.append(phrase)


def get_plugin_instance(plugin_class):
    info = None
    profile = {
        'prefers_email': False,
        'location': 'Cape Town',
        'timezone': 'US/Eastern',
        'phone_number': '012344321'
    }
    return plugin_class(info, profile)
