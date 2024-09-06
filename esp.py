from machine import Pin
import time
import dht
import network
import socket
import json


wifi = network.WLAN(network.STA_IF)

if not wifi.active():
    print("ligando wi-fi no esp")
    wifi.active(True)
    wifi.connect("nome_rede_wifi", "senha_rede_wifi")

while not wifi.isconnected():
        pass

if wifi.isconnected():
    print("Connected to Wi-Fi")
    print("IP address: ", wifi.ifconfig()[0])

dht_pin = Pin(12)
dht_sensor = dht.DHT22(dht_pin)

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request:", request)

    
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    data = {"temperature":temperature,"humidity":humidity}
    
    json_data = json.dumps(data)
    #BytesMsg = bytes(msg, "utf-8")
    
    response = "HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n" + json_data


    
    # Send the response to the client
    client_socket.send(response)

    # Close the client socket
    client_socket.close()
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen(5)
print("Server started. Listening on port 80.")

while True:
    try:
        # Wait for a client to connect
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)

        # Handle the client request
        handle_client(client_socket)
    except Exception as e:
        print("Error:", e)

    # Delay before handling the next client request
    time.sleep(1)
    
