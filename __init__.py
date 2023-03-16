# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
TODO add application name
TODO list voices with spd-say -L and parsing the output
subprocess spd-say version

Doc:
Requires speech-dispatcher and its Python bindings to be installed (the python3-speechd package on Debian 11.6 at time of this writing).

Speech Dispatcher is configured using separate config files. It allows for many customizations including different speech settings for different applications (Firefox, Emacs, and now Anki). See the Configuration section of the speech-dispatcher Texinfo document for file locations and examples.
/Doc

multiple voices (service) can be used and Anki should use the first one that works:
{{tts en_US voices=speechd,HyperTTS,gTTS:FieldName}}

TODO: handle {{tts en_US voices=speechd,gTTS:cloze-only:FieldName}}
"""

import os
import sys
from concurrent.futures import Future
from dataclasses import dataclass
from typing import List, cast

from anki.lang import compatMap
from anki.sound import AVTag, TTSTag
from aqt import mw
from aqt.sound import OnDoneCallback, av_player
#from aqt.tts import TTSProcessPlayer, TTSVoice

import subprocess
import aqt.tts

# we subclass the default voice object to store the speechd language code
@dataclass
class SpeechDVoice(aqt.tts.TTSVoice):
    speechd_lang: str

#class SpeechDPlayer(TTSProcessPlayer):
class SpeechDPlayer(aqt.tts.TTSProcessPlayer):
    # this is called the first time Anki tries to play a TTS file
    def get_available_voices(self) -> List[aqt.tts.TTSVoice]:
        voices = []
        # add the voice using the name "speechd"
        voices.append(SpeechDVoice(name="speechd", lang="en_US", speechd_lang="en-us"))
        return voices  # type: ignore

    # this is called on a background thread, and will not block the UI
    def _play(self, tag: AVTag) -> None:
        #get the avtag
        assert isinstance(tag, TTSTag)
        match = self.voice_for_tag(tag)

        # is the field blank?
        if not tag.field_text.strip():
            return

        #subprocess.run(["spd-say", tag.field_text])
        self._process = subprocess.Popen(
            ["spd-say", "-w", "-e", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # write the input text to stdin
        self._process.stdin.write(tag.field_text.encode("utf8"))
        self._process.stdin.close()
        self._wait_for_termination(tag)

        return

    # this is called on the main thread, after _play finishes
    #def _on_done(self, ret: Future, cb: OnDoneCallback) -> None:
        # close connection to the speech-dispatcher daemon
        #client = speechd.SSIPClient('Anki')
        #client.close()
        #pass

    # we don't support stopping while the file is being downloaded
    # (but the user can interrupt playing after it has been downloaded)
    def stop(self):
        pass


# register our handler
av_player.players.append(SpeechDPlayer(mw.taskman))
