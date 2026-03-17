from opcua import Client
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import json
import time

# ---------------- OPC UA ----------------
opc_url = "opc.tcp://127.0.0.1:49320"
opc_client = Client(opc_url)

# ---------------- AWS IoT ----------------
endpoint = "a5e1dq805jy0x-ats.iot.us-east-1.amazonaws.com"
cert = "C:/Users/srama/Downloads/device.pem.crt"
key = "C:/Users/srama/Downloads/private.pem.key"
root_ca = "C:/Users/srama/Downloads/AmazonRootCA1.pem"

client_id = "kepware-python-client"
topic = "factorydatasource/data"

# MQTT connection
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=cert,
    pri_key_filepath=key,
    ca_filepath=root_ca,
    client_bootstrap=client_bootstrap,
    client_id=client_id,
    clean_session=False,
    keep_alive_secs=30,
)

print("Connecting to AWS IoT...")
mqtt_connection.connect().result()
print("Connected to AWS IoT")

# ---------------- MAIN LOOP ----------------
try:
    opc_client.connect()
    print("Connected to Kepware")

    production_count = opc_client.get_node("ns=2;s=KepWare_Python_Connection.Machine_Runing_Staus.Production_Count")
    rejected_count = opc_client.get_node("ns=2;s=KepWare_Python_Connection.Machine_Runing_Staus.Rejected_Count")
    temperature = opc_client.get_node("ns=2;s=KepWare_Python_Connection.Machine_Runing_Staus.Temperatuer")

    while True:
        pc = production_count.get_value()
        rc = rejected_count.get_value()
        temp = temperature.get_value()

        # Create JSON payload
        payload = {
            "production_count": pc,
            "rejected_count": rc,
            "temperature": temp
        }

        print("Sending:", payload)

        # Publish to AWS IoT
        mqtt_connection.publish(
            topic=topic,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

        time.sleep(2)

finally:
    opc_client.disconnect()
    mqtt_connection.disconnect()
