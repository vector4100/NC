# -*- coding: utf-8 -*-
"""


This program intends to translate communication provided by a MODBUS device

@author: Victor
"""

def cp2(val,bits) -> int:
    
    result = int(val, bits)
    if result & (1 << (bits-1)):
        result -= 1 << bits
    return result

def divideWords(array) -> []:
    """Function to divide the message in groups of 4 characters which 
    corresponds to a word, this is done to facilitate further decoding"""
    size = len(array) 
    result_array = []
    #iterates thru array in increments of 4, and appends every 4 to new array
    for i in range(0,size,4):
        if i <= size-4:
            result_array.append(array[i:i+4])
        
    return result_array  

def crcCheck(msg):
    """TBD: Function to check CRC in message"""
    received_crc = msg[-4:]
    msg_to_check = msg[:-4]
    
    return 
        
def receivedMsgDecoder(msg) :
    """Function to decode a MODBUS COM string, 
    it can only translate hexadecimal messages into signed or 
    unsigned integers, information type must be:
    [0:2] = device
    [2:4] = mode
    [4:6] = size of information (amount of registers to read). 
    signed information is converted from hex to int by using twos complement"""
    
    ###Exceptions and error treatment
    if type(msg) != type("string"):
        raise TypeError("Data provided must be a string")
    if len(msg)<7:
        raise ValueError(f"Length of message is incompatible, expected size is longer than 16, actual size is {len(msg)}")
    if any([int(i,16)>15 for i in msg]):
        raise Exception() #This error management is redundant, because trying to cast a char bigger than "f" will automatically raise an error
        
    ###Functional code    
    device = msg[0:2]
    mode = msg[2:4]
    info_size = int(msg[4:6],16)  
    info = msg[6:6+(2*info_size)]
    info_cut = divideWords(info)  
    int_info = [cp2(hexe,16) for hexe in info_cut]
    print(f'Message from device {device}, in mode {mode}')
    print(f'Information size is {info_size} and contains values {int_info}')
    
    return device,mode,info_size,info_cut,int_info    

#%% Mensagem enviada ao medidor 
sent_msg = "0503c5700006f95b"
"""
A mensagem enviada ao medidor, segundo a tabela de registradores para 
comunicação fornecida é:
    05 - dispositivo de destino
    03 - modo de leitura
    C570 - endereço da função requisitada,  medição da potência ativa na fase 1
    0006 - número de registradores a serem lido na resposta, 6 registradores
    F95B - CRC
    
    A mensagem enviada requisita a medição da potência ativa, 
    que segundo a tabela de comunicação, define que o valor obtido é um 
    signed32, ou seja um valor inteiro com sinal de 32 bits.
    Portanto, será necessário utilizar lógica de conversão de valores negativos
    em hexadecimal.
"""
#%%

received_msg = "05030c000000e000000176000000e55726"
receivedMsgDecoder(received_msg)
    
