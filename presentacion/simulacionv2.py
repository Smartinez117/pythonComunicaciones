import socket

# Función para simular la capa de aplicación (enviar)
def application_layer(message):
    print("\n<----------------------- envio del mensaje------------------------------->\n")
    print(f"Capa de Aplicación (Enviar): Mensaje original: '{message}'")
    return message.encode('utf-8')  # Convertir a bytes

# Función para simular la capa de transporte (TCP) (enviar)
def transport_layer(data):
    tcp_header = f'TCP_HEADER: {len(data)} bytes'
    packet = tcp_header.encode('utf-8') + data
    print(f"Capa de Transporte (Enviar): Paquete con encabezado TCP: '{packet}'")
    return packet

# Función para simular la capa de red (IP) (enviar)
def network_layer(packet):
    ip_header = 'IP_HEADER: 192.168.1.1 -> 192.168.1.2'
    full_packet = ip_header.encode('utf-8') + packet
    print(f"Capa de Red (Enviar): Paquete con encabezado IP: '{full_packet}'")
    return full_packet

# Función para simular el envío del paquete
def send_packet(full_packet):
    # Aquí se simula el envío del paquete
    print(f"Enviando paquete: '{full_packet}'\n")
    print("<--------------recepcion del mensaje enviado---------------------->\n")
    return full_packet  # Retornar el paquete para simular recepción

# Función para simular la recepción del paquete
def receive_packet(full_packet):
    print(f"Recibiendo paquete: '{full_packet}'")
    packet = network_layer_receive(full_packet)
    return packet

# Función para simular la capa de red en recepción
def network_layer_receive(full_packet):
    ip_header_length = len('IP_HEADER: 192.168.1.1 -> 192.168.1.2')
    packet = full_packet[ip_header_length:]  # Extraer el paquete TCP
    print(f"Capa de Red (Recibir): Paquete sin encabezado IP: '{packet}'")
    return packet

# Función para simular la capa de transporte en recepción
def transport_layer_receive(packet):
    tcp_header_length = len('TCP_HEADER: 4 bytes')
    data = packet[tcp_header_length:]  # Extraer los datos
    print(f"Capa de Transporte (Recibir): Datos sin encabezado TCP: '{data}'")
    return data

# Función para simular la capa de aplicación en recepción
def application_layer_receive(data):
    message = data.decode('utf-8')  # Convertir bytes a string
    print(f"Capa de Aplicación (Recibir): Mensaje recibido: '{message}'")

# Simulación completa del proceso de envío y recepción
def simulate_communication():
    # Mensaje que se va a enviar
    message = "hola"
    
    # Proceso de envío
    data = application_layer(message)
    packet = transport_layer(data)
    full_packet = network_layer(packet)
    
    # Simular el envío del paquete y recibirlo en el servidor
    received_full_packet = send_packet(full_packet)
    
    # Proceso inverso (recepción)
    packet = receive_packet(received_full_packet)
    data = transport_layer_receive(packet)
    application_layer_receive(data)

# Ejecutar simulación de comunicación completa
simulate_communication()

