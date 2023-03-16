adding speech-dispatcher support to Anki through an add-on

`old-attempt` contains the first iteration which used the speechd python bindings. The current version uses subprocess and spd-say because, atleast on Debian 11.6, a separate package was required (python3-speechd). Future versions may return to the python bindings implementation.
