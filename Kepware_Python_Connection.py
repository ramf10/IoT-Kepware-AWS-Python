from opcua import Client,ua
import time

# OPC UA server address
url = "opc.tcp://127.0.0.1:49320"

client = Client(url)

try:
    client.connect()
    print("Connected to Kepware OPC UA Server")

    # Get nodes
    #motor_speed = client.get_node("KepWare_Python_Connection.Machine_Runing_Staus.Motor_Speed")
    production_count = client.get_node("ns=2;s=KepWare_Python_Connection.Machine_Runing_Staus.Production_Count")
    rejected_count = client.get_node("ns=2;s=KepWare_Python_Connection.Machine_Runing_Staus.Rejected_Count")
    temperature = client.get_node("ns=2;s=KepWare_Python_C
    while True:
onnection.Machine_Runing_Staus.Temperatuer")

        #ms = motor_speed.get_value()
        pc = production_count.get_value()
        rc = rejected_count.get_value()
        temp = temperature.get_value()

        #print("Motor Speed:", ms)
        print("Production Count:", pc)
        print("Rejected Count:", rc)
        print("Temperature:", temp)
        print("---------------------------")

        time.sleep(2)
        if pc > 150:
            print("Production Count exceeded limit")
        else:
            print("Production Line is Good")
            continue
finally:
    client.disconnect()