import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

# Инициализируем всё, что нужн

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(17, 1)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
D = [26, 19, 13, 6, 5, 11, 9, 10]

# Решил внести небольшие изменения в виде строки

GPIO.setup(21, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(1, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
B = [21, 29, 16, 12, 1, 7, 8, 25]

def decToBinList(decNumber):

    a = [0,0,0,0,0,0,0,0]
    b = int(decNumber)

    if decNumber >= 0 and decNumber <= 255 :
        for i in range(8):
            a[7-i] = b % 2
            b //= 2
        return(a)

# Сначала я перекопировал обе функции по отдельности

def num2leds(value):
    a = decToBinList(value)
    for i in range(8):
        GPIO.output(B[i], a[i])

def num2dac(value):
    Output = decToBinList(value)
    for i in range(8):
        GPIO.output(D[i], Output[i])

# Потом реализовал их совместно

def num2pins(pins, value):

    leds = decToBinList(pins)
    for i in range(8):
        GPIO.output(B[i], leds[i])
    
    voltage = decToBinList(value)
    for i in range(8):
        GPIO.output(D[i], voltage[i])

# Вставил для красоты, чтобы светодиоды загорались, пока заряжается)

def lightBar(number):

    count = 1
    while number > 16 + 32 * count:
        count += 1
    
    for i in range(8):
        GPIO.output(B[i], 0)

    for i in range(count):
        GPIO.output(B[i], 1)

def adc(mid = 128, counter = 6):

    # Задаём определяющий параметр
    # Проверяем значение в нем
    # Проверяем значение на единицу ниже

    sum = 0 
    num2dac(mid)
    time.sleep(0.01)
    if GPIO.input(4) == 0: 
        sum += 1
    num2dac(mid - 1) 
    time.sleep(0.01)
    if GPIO.input(4) == 0: 
        sum += 1
    
    # Если сумма равна 1, то это граничное значение и его мы выводим
    # Если нет, то по рекурсии выводим большее или меньшее значение соответственно

    if sum == 1:
        return mid
    else: 
        if sum == 2: return adc(mid=(mid - 2 ** counter), counter=(counter - 1))
        else: return adc(mid=(mid + 2 ** counter), counter=(counter - 1))

voltage = 0
measure = []
time_ = []
try:

    # Задаем начало отсчёта

    measure += [voltage]
    time_ += [time.clock()]
    GPIO.output(23, 1)

    # Заряжаем конденсатор

    while (voltage < 255):
        voltage = adc()
        measure += [voltage]
        time_ += [time.clock()]
        lightBar(voltage)
    
    # Разряжаем конденсатор
    
    GPIO.output(23, 0)
    while (voltage >= 0):
        voltage = adc()
        measure += [voltage]
        time_ += [time.clock()]
        lightBar(voltage)
    
    # Записываем данные измерений

    np.savetxt("data.txt", measure, fmt='%d')
    
    # Записываем среднее время и шаг квантования

    time_ = np.array(time_)

    dT = np.mean(time_)
    dV = 3.3 / (2 ** 8 - 1)
    task = open("settings.txt", 'w')
    task.write(dT)
    task.write("\n")
    task.write(dV)
    task.close()
    
    # Строим график

    plt.plot(time_, measure)
    plt.axis([0, round(np.max(time_) + 1), 0, round(np.max(measure) + 1)])
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.show()
    

finally:
    num2pins(0, 0)