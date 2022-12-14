# <p align="center">:heart:TIA</p>

This is a stripped down version of the [MIDIbox TIA](http://www.midibox.org/dokuwiki/doku.php?id=midibox_tia) ([PDF](Schematics/midibox_tia.pdf)). It uses a Raspberry Pi Pico and MicroPython to control the Atari 2600 TIA chip for some old-school sound goodness.

The clock signal to the TIA is provided by a PIO state machine instead of a crystal. Realtime modulation of the state machine frequency allows the TIA to output a continuous pitch instead of the original 32 pitches that were most of the time off-scale.

The next step is to add CVs for waveform, volume, and for pitch with 1V/oct.

# Schematics

![loveTIA schematics](Schematics/loveTIA_schematics.png)


(Old version)

[![vcTIA - Atari 2600 TIA and Arduino](https://img.youtube.com/vi/jGm9PULHrRM/0.jpg)](https://www.youtube.com/watch?v=jGm9PULHrRM)
