
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import typing as typ
    class GPIO:
        LOW = 0
        HIGH = 1

        OUT = 0
        IN = 1

        BOARD = 10
        BCM = 11

        PUD_OFF = 20
        PUD_DOWN = 21
        PUD_UP = 22

        RISING = 31
        FALLING = 32
        BOTH = 33

        SERIAL = 40
        SPI = 41
        I2C = 42
        HARD_PWM = 43

        @classmethod
        def setmode(cls, mode):
            print(f'RPI.GPIO.setmode -> {mode}')

        @classmethod
        def setwarnings(cls, flag):
            print(f'RPI.GPIO.setwarnings -> {flag}')

        @classmethod
        def setup(cls, channel, state, initial=LOW, pull_up_down=PUD_OFF):
            print(f'RPI.GPIO.setup -> {channel}, {state}, {initial}, {pull_up_down}')

        @classmethod
        def output(cls, channel, outmode):
            print(f'RPI.GPIO.output -> {channel}, {outmode}')

        @classmethod
        def input(cls, channel):
            print(f'RPI.GPIO.input -> {channel}')
            return True

        @classmethod
        def cleanup(cls, channel=None):
            print(f'RPI.GPIO.cleanup -> {channel}')

        @classmethod
        def wait_for_edge(cls, channel, event, timeout=None) -> typ.Optional[int]:
            print(f'RPI.GPIO.wait_for_edge -> {channel}, {event}, {timeout}')
            return channel

        @classmethod
        def add_event_detect(cls, channel, event, callback=None, bouncetime=None):
            print(f'RPI.GPIO.add_event_detect -> {channel}, {event}, {callback}, {bouncetime}')

        @classmethod
        def add_event_callback(cls, channel, callback, bouncetime=None):
            print(f'RPI.GPIO.add_event_callback -> {channel}, {callback}, {bouncetime}')

        @classmethod
        def event_detected(cls, channel) -> bool:
            print(f'RPI.GPIO.event_detected -> {channel}')
            return True

        @classmethod
        def remove_event_detect(cls, channel):
            print(f'RPI.GPIO.remove_event_detect -> {channel}')

        @classmethod
        def gpio_function(cls, channel):
            print(f'RPI.GPIO.gpio_function -> {channel}')
            return cls.IN

        class PWM:
            def __init__(self, channel, frequency):
                print(f'RPI.GPIO.PWM.__init__ -> {channel}, {frequency}')

            def start(self, duty_cycle):
                print(f'RPI.GPIO.PWM.start -> {duty_cycle}')

            def stop(self):
                print(f'RPI.GPIO.PWM.stop')

            def ChangeFrequency(self, frequency):
                print(f'RPI.GPIO.PWM.ChangeFrequency')

            def ChangeDutyCycle(self, duty_cycle):
                print(f'RPI.GPIO.PWM.ChangeDutyCycle -> {duty_cycle}')


GPIO.setmode(GPIO.BCM)


class Pin:
    def __init__(self, channel, state, initial=GPIO.LOW, pull_up_down=GPIO.PUD_OFF, cleanup=True):
        self.__channel = channel
        self.__state = state
        self.__initial = initial
        self.__pud = pull_up_down
        if cleanup:
            self.cleanup()
        if state == GPIO.IN:
            GPIO.setup(channel, state, pull_up_down=pull_up_down)
        elif state == GPIO.OUT:
            GPIO.setup(channel, state, initial=GPIO.LOW)
        else:
            raise ValueError("Not IN or OUT")

    def input(self) -> bool:
        return GPIO.input(self.__channel)

    def output(self, value: bool):
        GPIO.output(self.__channel, value)

    def cleanup(self):
        GPIO.cleanup(self.__channel)

    def wait_for_edge(self, event=GPIO.FALLING, timeout_ms=None) -> bool:
        ret = GPIO.wait_for_edge(self.__channel, event, timeout_ms)
        return ret is not None

    def add_event_detect(self, event, callback=None, bouncetime_ms=None):
        GPIO.add_event_detect(self.__channel, event, callback, bouncetime_ms)

    def add_event_callback(self, callback, bouncetime_ms=None):
        GPIO.add_event_callback(self.__channel, callback, bouncetime_ms)

    def event_detected(self) -> bool:
        return GPIO.event_detected(self.__channel)

    def remove_event_detect(self):
        GPIO.remove_event_detect(self.__channel)

    @property
    def channel(self):
        return self.__channel

    @property
    def state(self):
        return self.__state

    @property
    def initial(self):
        return self.__initial

    @property
    def pud(self):
        return self.__pud

    def __del__(self):
        self.cleanup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
