# RPi_GPIO_Helper
RPi.GPIO Helper Library.<br>
https://pypi.org/project/RPi-GPIO-Helper/

github<br>
https://github.com/taogya/RPi_GPIO_Helper

# Installation
```
# pip install RPi.GPIO
pip install RPi-GPIO-Helper
```

# Usage
```
# GPIO is used in same way as RPi.GPIO.
from RPi_GPIO_Helper import GPIO, Pin


out_pin = Pin(23, GPIO.OUT, initial=GPIO.LOW)
out_pin.output(True) # or out_pin.output(GPIO.HIGH)
# out_pin.cleanup()

in_pin = Pin(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ret = in_pin.input()
# in_pin.cleanup()
```
