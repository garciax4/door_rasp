#!/usr/bin/python
import time

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Define GPIO pins
out1 = 19
out2 = 6
D_ENABLE = 5    #enable do driver do stepper
POWER_motor = 17
relay_pin = 21

step_sleep = 0.001
step_count = 200

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT )
GPIO.setup(D_ENABLE, GPIO.OUT )
GPIO.setup(relay_pin, GPIO.OUT )
GPIO.setup(POWER_motor, GPIO.OUT)

# inicialização
GPIO.output( out1, GPIO.LOW )
GPIO.output( out2, GPIO.LOW )
GPIO.output( D_ENABLE, GPIO.HIGH )
GPIO.output(relay_pin, GPIO.LOW)
GPIO.output(POWER_motor, GPIO.LOW)

def cleanup():
    GPIO.output( out1, GPIO.LOW )
    GPIO.output( out2, GPIO.LOW )
    GPIO.output( D_ENABLE, GPIO.HIGH )
    GPIO.cleanup()

# Function to rotate the motor
def rodar():
    GPIO.output(POWER_motor, GPIO.HIGH)
    GPIO.output(D_ENABLE, GPIO.LOW)
    GPIO.output(relay_pin, GPIO.HIGH)
    if GPIO.input(out1)==0:
        GPIO.output(out1, GPIO.HIGH)
        control_porta=0
    else:
        GPIO.output(out1, GPIO.LOW)
        control_porta=1
    for _ in range(step_count):
        GPIO.output(out2, GPIO.HIGH)
        time.sleep(step_sleep)
        GPIO.output(out2, GPIO.LOW)

    GPIO.output(POWER_motor, GPIO.LOW)   
    GPIO.output(D_ENABLE, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(relay_pin, GPIO.LOW)


#le os ids do arquivo
def ler_lista_numeros(nome_arquivo):
    numeros = []
    try:
        with open(nome_arquivo,'r') as arquivo:
            for linha in arquivo:
                linha_limpa = linha.strip()
                if linha_limpa:
                    numeros.append(int(linha_limpa))
            return numeros
    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")
        return []

#escreve os novos ids no arquivo
def escrever_numeros(nome_arquivo):
    try:
        with open(nome_arquivo,'a') as arquivo:
            print("Waiting card...")
            time.sleep(0.5)
            id, _ = reader.read()
            print("Card Present!")
            numero_procurado = str(id)
            arquivo.write(numero_procurado + '\n')

    except FileNotFoundError:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado.")



# Define os nomes dos arquivo
nome_arquivo='/home/safe-door-n3e/Desktop/numero.txt'

# id da tag que escreve ids de cartoes na lista
write = 571359383393

# Inicializa o leitor RFID
reader=SimpleMFRC522()

try:
    while True:
        # Le os ids dos arquivos
        numero = ler_lista_numeros(nome_arquivo)
        print("Waiting card...")
        id, _ = reader.read()
        print("Card Present!")
        numero_procurado = id

        if numero_procurado in numero:
            print("Acess Granted!")
            rodar()

        else:
            print("Acess Denied!")
            # Adiciona o id á lista de ids verificados
        if numero_procurado == write:
            escrever_numeros(nome_arquivo)
            time.sleep(0.75)


except KeyboardInterrupt:
    GPIO.cleanup()
