import time
from apns import APNs, Frame, Payload

apns = APNs(use_sandbox=True, cert_file='/home/ec2-user/LocalTestCert.pem', key_file='/home/ec2-user/LocalTestKeyNP.pem', enhanced=True)

# Send a notification
token_hex = 'd6915bfdc113c048a04666f61b733916ec23ef6db0c0b2c1081ec9f721df8c33'
payload = Payload(alert="Hello World!", sound="default", badge=1)
apns.gateway_server.send_notification(token_hex, payload)

# Send multiple notifications in a single transmission
frame = Frame()
identifier = 1
expiry = time.time()+3600
priority = 10
apns.gateway_server
frame.add_item('d6915bfdc113c048a04666f61b733916ec23ef6db0c0b2c1081ec9f721df8c33', payload, identifier, expiry, priority)
apns.gateway_server.send_notification_multiple(frame)

