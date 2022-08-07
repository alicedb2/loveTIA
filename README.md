# vcTIA - Voltage Controlled TIA chip

[![vcTIA - Atari 2600 TIA and Arduino](https://img.youtube.com/vi/jGm9PULHrRM/0.jpg)](https://www.youtube.com/watch?v=jGm9PULHrRM)

Barebone Arduino setup that controls the Atari 2600 TIA chip.

It is based on the core circuit of the MIDIbox TIA. It uses two 74HC595 shift registers in series to write to the address and data buses on the TIA. The oscillator circuit is based on the Rev14/15 A2600 motherboard and uses the original 3.58 MHz NTSC crystal instead of the original oscillator circuit used by MIDIbox.
