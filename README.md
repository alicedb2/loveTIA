# :heart:TIA

This is a stripped down version of the [MIDIbox TIA]. It uses a Raspberry Pi Pico and MicroPython to control an Atari 2600 TIA chip for some old-school sound goodness.

The clock signal to the TIA is provided by a PIO state machine instead of a crystal. Realtime modulation of the state machine frequency allows the TIA to output a continuous pitch instead of the original 32 pitches that were most of the time off-scale.

The next step is to add CVs for waveform, volume, and for pitch with 1V/oct.


(Old version)

[![vcTIA - Atari 2600 TIA and Arduino](https://img.youtube.com/vi/jGm9PULHrRM/0.jpg)](https://www.youtube.com/watch?v=jGm9PULHrRM)
