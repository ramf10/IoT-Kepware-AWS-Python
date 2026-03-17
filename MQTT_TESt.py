from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

endpoint = "a5e1dq805jy0x-ats.iot.us-east-1.amazonaws.com"
cert = "C:/Users/srama/Downloads/device.pem.crt"
key = "C:/Users/srama/Downloads/private.pem.key"
root_ca = "C:/Users/srama/Downloads/AmazonRootCA1.pem"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=cert,
    pri_key_filepath=key,
    ca_filepath=root_ca,
    client_id="test-client",
)

print("Connecting...")
mqtt_connection.connect().result()
print("Connected successfully!")
