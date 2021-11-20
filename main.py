import umqtt_robust2
import GPSfunk
from NPfunc import set_color
import buzzer
from machine import Pin
from time import sleep_ms, sleep, ticks_ms
sleep(0.5)
gps_interval = 6000
gps_start = ticks_ms()
gps = Pin(16, Pin.OUT)
lib = umqtt_robust2

tilt_sensor = Pin(22, Pin.IN)
sleep(0.5)

# opret en ny feed kaldet map_gps indo på io.adafruit
mapFeed = bytes('{:s}/feeds/{:s}'.format(b'Hjordt', b'mapfeed/csv'), 'utf-8')
sleep(0.5)
# opret en ny feed kaldet speed_gps indo på io.adafruit
speedFeed = bytes('{:s}/feeds/{:s}'.format(b'Hjordt', b'speedfeed/csv'), 'utf-8')
sleep(0.5)
# opretter et nyt feed kaldet accelfeed på io.adafruit
faldFeed = bytes('{:s}/feeds/{:s}'.format(b'Hjordt', b'faldfeed/csv'), 'utf-8')
sleep(0.5)
while True:
    besked = lib.besked
    sleep(1)
    if lib.c.is_conn_issue():
        while lib.c.is_conn_issue():
            # hvis der forbindes returnere is_conn_issue metoden ingen fejlmeddelse
            lib.c.reconnect()
        else:
            lib.c.resubscribe()
    try:
        
        if ticks_ms() - gps_start >= gps_interval:
            
            lib.c.publish(topic=mapFeed, msg=GPSfunk.main())
            speed = GPSfunk.main()
            speed = speed[:4]
            print("speed: ",speed)
            lib.c.publish(topic=speedFeed, msg=speed)
            gps_start = ticks_ms()
            print(str(tilt_sensor.value()))
            tilt = str(tilt_sensor.value())
            print(type(tilt))
            lib.c.publish(topic=faldFeed, msg=tilt)
            
        if besked == "rød":
            buzzer.buzzer_set() 
            sleep(1)
            set_color(255, 0, 0)
            buzzer.buzzer_clear()
            sleep(5)
            set_color(0, 0, 0)
            lib.besked = ""
        if besked == "grøn":
            buzzer.buzzer_set() 
            sleep(1)
            set_color(0, 255, 0)
            buzzer.buzzer_clear()
            sleep(5)
            set_color(0, 0, 0)
            lib.besked = ""
        if besked == "blå":
            buzzer.buzzer_set() 
            sleep(1)
            set_color(0, 0, 255)
            buzzer.buzzer_clear()
            sleep(5)
            set_color(0, 0, 0)
            lib.besked = ""
        if besked == "lilla":
            buzzer.buzzer_set() 
            sleep(1)
            set_color(153, 50, 204)
            buzzer.buzzer_clear()
            sleep(5)
            set_color(0, 0, 0)
            lib.besked = ""
        if besked == "orange":
            buzzer.buzzer_set() 
            sleep(1)
            set_color(255, 69, 0)
            buzzer.buzzer_clear()
            sleep(5)
            set_color(0, 0, 0)
            lib.besked = ""
        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        lib.c.disconnect()
        lib.wifi.active(False)
        lib.sys.exit()
    except OSError as e:
        print('Failed to read sensor.')
#     except NameError as e:
#         print('NameError')
#     except TypeError as e:
#         print('TypeError')
    lib.c.check_msg() # needed when publish(qos=1), ping(), subscribe()
    lib.c.send_queue()  # needed when using the caching capabilities for unsent messages

lib.c.disconnect()
