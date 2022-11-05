import time
import machine
from machine import Pin, SoftI2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import dht

interruptCounter = 0

led = Pin(22, Pin.OUT)
led_r = Pin(27, Pin.OUT)
led_a = Pin(25, Pin.OUT)
led_v = Pin(26, Pin.OUT)
soil_m = ADC(Pin(35))
soil_m.atten(ADC.ATTN_11DB)

led.value(0)
led_r.value(0)
led_a.value(0)
led_v.value(0)


i2c = SoftI2C(scl=Pin(19), sda=Pin(23))
sensor1 = dht.DHT11(Pin(5))

oled = SSD1306_I2C(128, 64, i2c)

#led.fill(1)
#oled.show()
#oled.text('Hola!!', 0, 10)
#oled.show()

def external_interrupt_1 (pin):
    global interruptCounter
    time.sleep(0.1)

    if interruptCounter == 0:
        led_a.value(0)
        led_r.value(1)
        led_v.value(0)
        state = machine.disable_irq()
        interruptCounter = 1
        machine.enable_irq(state)
    elif interruptCounter ==1:
        led_a.value(1)
        led_r.value(0)
        led_v.value(0)
        state = machine.disable_irq()
        interruptCounter = 2
        machine.enable_irq(state)
    else:
        led_a.value(0)
        led_r.value(0)
        led_v.value(1)
        state = machine.disable_irq()
        interruptCounter = 0
        machine.enable_irq(state)

Boton1 = Pin (14, Pin.IN, pull=Pin.PULL_UP)
Boton1.irq (trigger=Pin.IRQ_FALLING, handler=external_interrupt_1)


def tick(timer):                
    global led
    led.value(not led.value())

timer = Timer(0)
timer.init(period=100, mode=Timer.PERIODIC, callback=tick)


while True:
  try:
    sensor1.measure()
    temp = sensor1.temperature()
    hum = sensor1.humidity()
    soil_value = soil_m.read()
    soil_value = (4095-soil_value)/40.95
    oled.fill(0)
    oled.show()
    oled.text('Temperatura:', 0, 0)
    oled.text('  '+str(float(temp))+" C", 0, 10)
    oled.text('Humedad rel:', 0, 20)
    oled.text('  '+str(float(hum))+'%', 0, 30)
    oled.text('Humedad suelo:', 0, 40)
    oled.text('  '+str(float(soil_value))+'%', 0, 50)
    oled.show()
    
    time.sleep(5)
  except OSError as e:
    print(str(e))



  