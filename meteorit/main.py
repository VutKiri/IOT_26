import machine
import time
import neopixel
import uselect, sys
import BG77
import _thread
import os
import ahtx0
import random
from machine import Pin, I2C
import ujson


##############################################
##############################################
#########od sud test##########################
i2c1 = I2C(1, scl = Pin(15), sda = Pin(14), freq = 400000)

tmp_sensor = ahtx0.AHT20(i2c1)
tmp_sensor.initialize()
ran_wind = random.randint(20, 50)

#Creates JSON from the available peripherals
def createJSON():
    json_string={"temperature":tmp_sensor.temperature,"humidity":tmp_sensor.relative_humidity}
    json = ujson.dumps(json_string)
    return json

ticks_start = time.ticks_ms()
get_ticks_start = time.ticks_ms()
get_period = 6500
send_period = 15000#ms


        




###########posem test##############################
###################################################
###################################################

def core2_task():
    sel0 = machine.Pin(2, machine.Pin.OUT)
    sel1 = machine.Pin(3, machine.Pin.OUT)

    sel0.value(0)
    sel1.value(1)

    adc = machine.ADC(0)

    uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))
    VREF=3.3
    while True:
        read_adc = adc.read_u16()
        '''
        if read_adc > 65000:
            sel0.value(1)
        elif read_adc < 42000:
            sel0.value(0)
        '''
        #print(str(read_adc))
        uart.write(str(time.ticks_ms())+ "," + str(read_adc)+"\r")
        time.sleep(0.001)
    
    

spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)

RGB_LEDS = neopixel.NeoPixel(machine.Pin(16), 3, bpp=4)

RGB_LEDS[0] = (10,0,0,0)
RGB_LEDS[1] = (0,10,0,0)
RGB_LEDS[2] = (0,0,10,0)

RGB_LEDS.write()

pon_trig = machine.Pin(9,machine.Pin.OUT)


##to je moje##############
########################
def odesli_na_thingsboard():
    token = "VgEuJgBrVmg7NBmWqxl7"
    global ticks_start
    msg_ctr = 0
    while msg_ctr < 4:
        # 2. Přidávání (Akce 1, Index 0-3, Option ID 11, Hodnota)
        # ZKUSÍME TO BEZ UVOZOVEK - přesně podle tvé nápovědy <opt_value>
        
        #If it is time to send data, create JSON and send it to the server
        if (time.ticks_diff(time.ticks_ms(),ticks_start) >= send_period):
            ticks_start=time.ticks_ms()
            bg_uart.write(f'AT+QCOAPOPTION=0,0,0,11,\"api/v1/VgEuJgBrVmg7NBmWqxl7/telemetry\"\r\n')
            time.sleep(5)
            zprava = createJSON()
            #sendPostRequest(client, json)
            #sendPostRequest(client, "{\"temperature\":25}")
            msg_ctr += 1
            print(zprava)
            prikaz = f'AT+QCOAPSEND=0,1,2,1,{len(zprava)}\r\n'
            bg_uart.write(prikaz)
            time.sleep(1.5)
            bg_uart.write(zprava)
            bg_uart.write(b'\x1a')
    
    
########################
######posem#############




# machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5), timeout=200, timeout_char=5)
bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rxbuf=256, rx=machine.Pin(1), timeout = 0, timeout_char=1)

bg_uart.write(bytes("AT\r\n","ascii"))
print(bg_uart.read(10))


module = BG77.BG77(bg_uart, verbose=True, radio=False)

time.sleep(0.3)
module.sendCommand("AT+QURCCFG=\"urcport\",\"uart1\"\r\n")
time.sleep(0.1)
module.sendCommand("AT+CPSMS=0\r\n")
time.sleep(2)
module.sendCommand("AT+CEDRXS=0\r\n")
time.sleep(3)
module.sendCommand("AT+QCFG=\"band\",0x0,0x80084,0x80084,1\r\n")
module.setRadio(1)
module.setAPN("lpwa.vodafone.iot")
time.sleep(3)
##to je moje##############
########################

module.sendCommand("AT+CGDCONT=1,\"IP\",\"lpwa.vodafone.iot\"\r\n")
time.sleep(3)
module.sendCommand("AT+CFUN=1\r\n")
time.sleep(3)
module.sendCommand("AT+QICSGP=1,1,\"lpwa.vodafone.iot\"\r\n")
time.sleep(3)
module.sendCommand("AT+QIACT?\r\n")
time.sleep(3)
module.sendCommand("AT+QIDEACT=1\r\n")
time.sleep(3)
module.sendCommand("AT+QIACT=1\r\n")
time.sleep(3)
module.sendCommand("AT+QCOAPCFG=\"pdpcid\",0,1\r\n")
time.sleep(3)
module.sendCommand("AT+QCOAPCFG=\"pdpcid\",0,1\r\n")
time.sleep(0.3)
module.sendCommand("AT+QCOAPOPEN=0,\"147.229.148.105\",5683\r\n")
time.sleep(7)
odesli_na_thingsboard()
########################
######posem#############

#module.setOperator(BG77lpwa.vodafone.iot.COPS_MANUAL, BG77.Operator.CZ_VODAFONE)


def read1():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

def readline():
    c = read1()
    buffer = ""
    while c != None:
        buffer += c
        c = read1()
    return buffer


def waitForCEREG():
    data_out = ""
    while True:
        data_tmp = bg_uart.read(1)
        if data_tmp:
            data_out = data_out + str(data_tmp, 'ascii')
        if "+CEREG: 5" in data_out:
            time.sleep(.01)
            data_tmp = bg_uart.read()
            data_out = data_out + str(data_tmp, 'ascii')
            return

#waitForCEREG()
print("OUT")
'''
print(f"Init: {time.ticks_ms()}")
while True:
    data = bg_uart.read()
    print(f"{time.ticks_ms()} {data}")
    time.sleep(1)
'''


module.sendCommand("AT+QCSCON=1\r\n")

#second_thread = _thread.start_new_thread(core2_task, ())

print("Terminal Ready")

while True:
    try:
        data = readline()
        if len(data) != 0:
            if "WKUP" in data.upper():
                pon_trig.value(1)
                time.sleep(.3)
                pon_trig.value(0)
            elif "TIME" in data:
                print(time.ticks_ms())
            elif "STOP" in data:
                os.exit()
            else:
                print(f"{time.ticks_ms()}: -> " + data.strip("\r\n"))
                bg_uart.write(data[:len(data)-2].encode())
                bg_uart.write("\r\n")
        if bg_uart.any():
            time.sleep(.01)
            data = bg_uart.read()
            #print(data)
            if data != None:
                #data = data.decode()
                #print(data)
                if 0xff in data:
                    m = bytearray(data)
                    for i in range(len(m)):
                        if m[i] == 0xff:
                            m[i] = 0
                    data = bytes(m)
                data = str(data, 'ascii')
                data = data.strip('\r\n')
                data_split = data.split("\n")
                for line in data_split:
                    if line == "\r\n":
                        continue
                    print(f"{time.ticks_ms()}: <- {line.strip('\r\n')}")
        time.sleep(.1)
    except KeyboardInterrupt:
        break
    except:
        pass


