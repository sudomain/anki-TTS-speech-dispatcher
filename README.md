# Anki TTS Speech Dispatcher
Adding speech-dispatcher support to Anki through an add-on. It uses `spd-say` to speak text, so if that works then this add-on should work.

This add-on is new and hasn't been extensively test. It assumes you have a properly configured speech-dispatcher and that `spd-say` works (this add-on uses the default voice). Some limitations which I hope to fix:
1. "en_US" is hardcoded into the add-on though isn't used. If speechd is configured to use another language, it should work, but specifying different languages in the field should have no effect e.g. `{{tts fr_FR:SomeField}}`
2. Field TTS speed control is not yet supported e.g. `{{tts fr_FR speed=0.8:SomeField}}`
3. config file - add variable so reading can be disabled while reviewing

Speech Dispatcher is configured using separate config files. It allows for many customizations including different speech settings for different applications (Firefox, Emacs, and now Anki). It works with many TTS engines. If an engine is not already supported, the process of making a new one is relatively simple using the "generic output module". See the Configuration section of the speech-dispatcher Texinfo document for file locations and examples.

## Multiple voices
According to Anki's manual, multiple voices can be specified and Anki should use the first available one:
`{{tts en_US voices=speechd,HyperTTS,gTTS,Apple_Otoya,Microsoft_Haruka:FieldName}}`

Note: AnkiDroid doesn't yet support this sytax 

## Files
`old-attempt/` contains the first iteration which used the speechd python bindings. The current version uses subprocess and spd-say because, atleast on Debian 11.6, a separate package was required (python3-speechd). Future versions may return to the python bindings implementation.
