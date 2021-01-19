import time
import RPi.GPIO as GPIO
GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )
 
clock_pin = 15
data_pin = 14
 
GPIO.setup( clock_pin, GPIO.OUT )
GPIO.setup( data_pin, GPIO.OUT )
 
def apa102_send_bytes( clock_pin, data_pin, bytes_ ):
    """
    zend de bytes naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
    """
 
    # implementeer deze functie:
 
    # zend iedere byte in bytes:
    assert len(bytes_) == 4
    for byte in bytes_:
    #    zend ieder bit in byte:
#        print(byte)
        assert len(byte) == 8
        for bit in byte:
            GPIO.output(data_pin, bit)
            #time.sleep(.1)
            GPIO.output(clock_pin, 1)
            #time.sleep(.1)
            GPIO.output(clock_pin, 0)
    #       maak de data pin hoog als het bit 1 is, laag als het 0 is
    #       maak de clock pin hoog
    #       maak de clock pin laag
 
 
def apa102( clock_pin, data_pin, colors ):
    """
    zend de colors naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
 
    De colors moet een list zijn, met ieder list element een list van 3 integers,
    in de volgorde [ blauw, groen, rood ].
    Iedere kleur moet in de range 0..255 zijn, 0 voor uit, 255 voor vol aan.
 
    bv: colors = [ [ 0, 0, 0 ], [ 255, 255, 255 ], [ 128, 0, 0 ] ]
    zet de eerste LED uit, de tweede vol aan (wit) en de derde op blauw, halve strekte.
    """
 
    # implementeer deze functie, maak gebruik van de apa102_send_bytes functie
 
    # zend eerst 4 bytes met nullen
    def repeat_byte(val,r=8):
        return [val]*r
    start_frame = repeat_byte(repeat_byte(0), r=4)
    apa102_send_bytes(clock_pin, data_pin, start_frame)
    for color in colors:
        color_data = [repeat_byte(1)] + [list(map(int, bin(256+c)[3:])) for c in color ]
       # apa102_send_bytes(clock_pin, data_pin, [ same_byte(1) ]
        apa102_send_bytes(clock_pin, data_pin, color_data)
    #    dan de 3 bytes met de kleurwaarden
    apa102_send_bytes(clock_pin, data_pin, repeat_byte(repeat_byte(1), r=4))
    time.sleep(2)
    # zend nog 4 bytes, maar nu met allemaal enen
 
blue = [ 255, 0, 0 ]
green = [ 0, 255, 0 ]
red = [ 0, 0, 255 ]
 
 
def flag(c):
    apa102(clock_pin, data_pin, [c]*8)
    time.sleep(1)