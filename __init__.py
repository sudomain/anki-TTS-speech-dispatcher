# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Speech Dispatcher is configured using separate config files. It allows for many customizations including different speech settings for different applications (Firefox, Emacs, and now Anki). It works with many TTS engines. If an engine is not already supported, the process of making a new one is relatively simple using the "generic output module". See the Configuration section of the speech-dispatcher Texinfo document for file locations and examples.

Heavily based on MacTTSPlayer(TTSProcessPlayer): https://github.com/ankitects/anki/blob/f9126927b1c537f76b2e11f2f8a6003d2313245b/qt/aqt/tts.py#L170
"""

# `info spd-say` should have most of the information needed to complete this TODO list, I just need more time
#TODO spd-say --pipe-mode might give better performance since it will keep an instance of spd-say reading from stdin and we can write to that using subprocess. There's an example in old-attempts/ directory
#TODO list voices with spd-say -L and parsing the output tab separated value of "NAME LANGUAGE VARIANT" however we need to account for NAME containing spaces such as "Chinese (Mandarin)"
#TODO remove hardcoded language "en_US" using spd-say --language 
#TODO test stopping with an output module known to support it such as espeak
#TODO remove unnecesary imports
#TODO support per field TTS speed e.g. {{tts fr_FR speed=0.8:SomeField}}. spd-say --rate can take values between -100 and 100 so the decimal values Anki uses must be normalizaed to integers between -100 and 100 

import subprocess
from dataclasses import dataclass
from typing import List, cast

from anki.sound import AVTag, TTSTag
from aqt import mw
from aqt.sound import OnDoneCallback, av_player

import aqt.tts

# we subclass the default voice object to store the speechd language code
@dataclass
class SpeechDVoice(aqt.tts.TTSVoice):
    #TODO Getting the voice list from `spd-say --list-synthesis-voices` can take several seconds if many are installed, so do it at Anki startup
    speechd_lang: str

#class SpeechDPlayer(TTSProcessPlayer):
class SpeechDPlayer(aqt.tts.TTSProcessPlayer):
    # this is called the first time Anki tries to play a TTS file
    def get_available_voices(self) -> List[aqt.tts.TTSVoice]:
        voices = []

        # add the voice using the name "speechd"
        voices.append(SpeechDVoice(name="speechd", lang="en_US", speechd_lang="en"))
        return voices  # type: ignore

    # this is called on a background thread, and will not block the UI
    def _play(self, tag: AVTag) -> None:
        #get the avtag
        assert isinstance(tag, TTSTag)
        match = self.voice_for_tag(tag)

        # is the field blank?
        if not tag.field_text.strip():
            return

        subprocess.run(["spd-say", "--wait", "--application-name", "Anki", tag.field_text])
        return

    # this is called on the main thread, after _play finishes
    # It seems it's only really necessary if the intention is to create temporary files. Instead, this add-on uses a subprocess.
    #def _on_done(self, ret: Future, cb: OnDoneCallback) -> None:
        #pass

    # we don't support stopping while the file is being downloaded
    # (but the user can interrupt playing after it has been downloaded)
    def stop(self):
        pass


# register our handler
av_player.players.append(SpeechDPlayer(mw.taskman))
