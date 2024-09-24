import random
import time

class Packet:
    def __init__(self, data):
        self.data = data
        self.sequence_number = random.randint(1, 1000)

class TCP:
    def __init__(self):
        self.sent_packets = []
        self.acknowledged_packets = []

    def send_packet(self, packet):
        print(f"Enviando paquete: {packet.data}, Número de secuencia: {packet.sequence_number}")
        self.sent_packets.append(packet)

    def receive_ack(self, sequence_number):
        print(f"Recibiendo ACK para el paquete: {sequence_number}")
        self.acknowledged_packets.append(sequence_number)

class IP:
    def __init__(self):
        self.tcp_layer = TCP()

    def send(self, packet):
        # Simula la posibilidad de pérdida de paquetes
        if random.random() > 0.1:  # 90% de probabilidad de éxito
            self.tcp_layer.send_packet(packet)
            time.sleep(1)  # Simula el tiempo de transmisión
            self.tcp_layer.receive_ack(packet.sequence_number)
        else:
            print(f"Paquete perdido: {packet.data}")

# Simulación
def simulate_tcp_ip():
    ip_layer = IP()
    for i in range(5):  # Enviar 5 paquetes
        packet = Packet(f"Datos {i+1}")
        ip_layer.send(packet)

simulate_tcp_ip()