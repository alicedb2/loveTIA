import rp2
from time import sleep
from machine import Pin, freq, mem32, ADC

### Address bus constants ###
# A2600 waveform addresses
ADDR_CTRL0 = 0b0101
ADDR_CTRL1 = 0b0110
# A2600 pitch addresse
# Allow to set divisors of
# a fundamental frequency
# (something between 30-32kHz, not sure)
ADDR_FREQ0 = 0b0111
ADDR_FREQ1 = 0b1000
# A2600 volume addresses
ADDR_VOL0 = 0b1001
ADDR_VOL1 = 0b1010


unique_waveforms = (1, 2, 3, 4, 6, 7, 8, 12, 14, 15)

tia_rw_pin = Pin(5, Pin.OUT, value=0)
addr_pins = [Pin(i, Pin.OUT, value=0) for i in (6, 7, 8, 9)]
data_pins = [Pin(i, Pin.OUT, value=0) for i in (10, 11, 12, 13, 14)]

adc_waveform = ADC(Pin(27))
adc_pitch = ADC(Pin(26))
adc_divisor = ADC(Pin(28))
#adc_volume = ADC(Pin())

##########################################################
## Start oscillator to original Atari 2600 NTSC 3.58MHz ##
##########################################################
# This calculates the required state machine
# clock division given a target clock frequency
def sm_div_calc(target_f):
    # We multiply by two because the PIOX
    # state machine contains 2 instructions
    target_f *= 2
    if target_f < 0:
        division = 256
    elif target_f == 0:
        # Special case: set clkdiv to 0.
        division = 0
    else:
        division = freq() * 256 // target_f
        if division <= 256 or division >= 16777216:
            raise ValueError("freq out of range")
    return division << 8


# A2600 NTSC crystal frequency
ATARI_FREQ = 3_579_545

# This is the RP2040/Pico register
# that will allow us to change
# the clock division of state machine 0
# on the fly without having to restart
# the state machine
ADDR_SM0_CLKDIV = 0x50200000 + 0x0C8


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def squarewave():
    set(pins, 1)
    set(pins, 0)

sm0 = rp2.StateMachine(0, squarewave, freq=freq(), set_base=Pin(17))
sm0.active(1)


def set_clock_freq(target_freq=ATARI_FREQ):
    mem32[ADDR_SM0_CLKDIV] = sm_div_calc(int(target_freq))


##########################################################


def loop(voice=2):
    last_volume_val = -1
    last_pitch_val = -1
    last_divisor_val = -1
    last_waveform_val = -1

    setVolume(15, voice)

    while True:
        sleep(0.05)

        # Volume
        #pot_read = oversampled_read(adc_volume, 4)
        #volume_val = binval(pot_read, 300, 60000, 16)
        #if volume_val != last_volume_val:
        #    setVolume(volume_val, voice)
        #    last_volume_val = volume_val
        #    print(f"volume_{volume_val} pot_{pot_read} div_{divisor}")

        # Pitch
        pot_read = oversampled_read(adc_pitch, 4)
        pitch_val = binval(pot_read, 300, 60000, 32)
        if pitch_val != last_pitch_val:
            setPitch(pitch_val + 1, voice)
            last_pitch_val = pitch_val
            # print(f"pitch_{pitch_val} pot_{pot_read}")

        # Clock divisor
        divisor_val = oversampled_read(adc_divisor, 4)
        if divisor_val != last_divisor_val:
            divisor = map(divisor_val, 300, 60000, 1, 128)
            set_clock_freq(ATARI_FREQ/divisor)
            last_divisor_val = divisor_val
            # print(f"potread_{divisor_val} divisor_{divisor}")


        # Waveform
        pot_read = oversampled_read(adc_waveform, 4)
        waveform_val = binval(pot_read, 300, 60000, 10)
        if waveform_val != last_waveform_val:
            setWaveform(waveform_val, voice)
            last_waveform_val = waveform_val
            # print(f"waveform_{waveform_val} pot_{pot_read}")


def map(value, input_min, input_max, output_min, output_max):

    if value < input_min: return output_min
    if value > input_max: return output_max

    out_val = (value - input_min) * (output_max - output_min) / (
        input_max - input_min
    ) + output_min
    return out_val


def binval(value, input_min, input_max, nb_bins):
    bin_width = (input_max - input_min) / nb_bins
    return max(0, min(nb_bins - 1, int((value - input_min) / bin_width)))


def oversampled_read(adc, nb_oversampling_bits):
    pot_read = 0
    for k in range(2 ** nb_oversampling_bits):
        pot_read += adc.read_u16()
    pot_read >>= nb_oversampling_bits
    return pot_read


def setTIApins(address, data):
    for bit, pin in enumerate(addr_pins):
        pin.value(address >> bit & 1)
    for bit, pin in enumerate(data_pins):
        pin.value(data >> bit & 1)


# volume from 0b0000 = 0 to 0b1111 = 15
def setVolume(volume, voice=2):

    volume = int(volume)

    if volume < 0 or volume > 15:
        print("Volume values should be between 0 and 15")
        return

    if voice == 0 or voice == 2:
        tia_rw_pin.high()
        setTIApins(ADDR_VOL0, volume)
        tia_rw_pin.low()
    sleep(0.001)
    if voice == 1 or voice == 2:
        tia_rw_pin.high()
        setTIApins(ADDR_VOL1, volume)
        tia_rw_pin.low()


# raw waveform from 0b0000 = 0 to 0b1111 = 15
# unique waveforms from 0 to 10
def setWaveform(waveform, voice=2):

    waveform = int(waveform)

    if waveform < 0 or waveform > 9:
        print("Waveform values should be between 0 and 9")
        return

    if voice == 0 or voice == 2:
        tia_rw_pin.high()
        setTIApins(ADDR_CTRL0, unique_waveforms[waveform])
        tia_rw_pin.low()
        sleep(0.001)
    if voice == 1 or voice == 2:
        tia_rw_pin.high()
        setTIApins(ADDR_CTRL1, unique_waveforms[waveform])
        tia_rw_pin.low()


# divisor from 0b00000 = 1 to 0b11111 = 32
# divides fundamental frequency ~30kHz
def setPitch(divisor, voice=2):

    divisor = int(divisor)

    if divisor < 1 or divisor > 32:
        print("Divisor values should be between 1 and 32")
        return

    if voice == 0 or voice == 2:
        tia_rw_pin.high()
        setTIApins(ADDR_FREQ0, divisor - 1)
        tia_rw_pin.low()
    sleep(0.001)
    if voice == 1 or voice == 2:
        tia_rw_pin.high()
        setTIApins(ADDR_FREQ1, divisor - 1)
        tia_rw_pin.low()


