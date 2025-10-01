from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import PWMLED, Device
from flask import Flask, render_template

app = Flask(__name__)

# Specify to use PiGPIO so PWM is done via hardware
Device.pin_factory = PiGPIOFactory()

LED_GPIO = 18 # GPIO pin connected to the LED. Use a pin that supports PWM if possible.
led = PWMLED(LED_GPIO)

led_locked = False

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/led/status')
def led_status():
    return {
        "brightness": led.value,
        "locked": led_locked
    }, 200
    
@app.route('/led/off')
def turn_off_led():
    global led_locked
    if led_locked:
        return "LED is locked", 403
    led.off()
    return "LED turned off", 200

@app.route('/led/on')
def turn_on_led():
    global led_locked
    if led_locked:
        return "LED is locked", 403
    led.on()
    return "LED turned on", 200
    
@app.route('/led/lock')
def lock_led():
    global led_locked
    led_locked = True
    return "LED is now locked", 200

@app.route('/led/unlock')
def unlock_led():
    global led_locked
    led_locked = False
    return "LED is now unlocked", 200

@app.route('/led/<brightness>')
def set_led_brightness(brightness):
    try:
        global led_locked
        if led_locked:
            return "LED is locked", 403
        brightness_value = float(brightness) / 100.0
        if 0.0 <= brightness_value <= 1.0:
            led.value = brightness_value
            return f"LED brightness set to {brightness_value}", 200
        else:
            return "Brightness value must be between 0.0 and 1.0", 400
    except ValueError:
        return "Invalid brightness value", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)