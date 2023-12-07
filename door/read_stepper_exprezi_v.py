#!/usr/bin/python
import time

from mfrc522 import SimpleMFRC522
import gpiozero

# Define GPIO pins
out1_pin = 19
out2_pin = 6
D_ENABLE_pin = 5    #enable do driver do stepper
POWER_motor_pin = 17
relay_pin = 21

step_sleep = 0.001
step_count = 200

# setup
out1 = gpiozero.DigitalOutputDevice(out1_pin)
out2= gpiozero.DigitalOutputDevice(out2_pin)
D_ENABLE= gpiozero.DigitalOutputDevice(D_ENABLE_pin,initial_value = True )
relay= gpiozero.DigitalOutputDevice(relay_pin)
POWER_motor = gpiozero.DigitalOutputDevice(POWER_motor_pin)


def cleanup():
	out1.off()
	out2.off()
	D_ENABLE.on()

# Function to rotate the motor
def rodar():
    POWER_motor.on()
    D_ENABLE.off()
    relay.on()
    if out1.value==0:
        out1.on()
        control_porta=0
    else:
        out1.off()
        control_porta=1
    for _ in range(step_count):
        out2.on()
        time.sleep(step_sleep)
        out2.off()

    POWER_motor.off()   
    D_ENABLE.on()
    time.sleep(3)
    relay.off()


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
		print(f"Acess Denied! to {id}")
		# Adiciona o id á lista de ids verificados
	if numero_procurado == write:
		escrever_numeros(nome_arquivo)
		time.sleep(0.75)

