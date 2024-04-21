from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = 'f65af3e8f227b4a24e3abe88ab35835cf20a9523ee3b6b43054c309ffaac588d' # found on Discord Application -> General Information page
PING_PONG = { 'type': 1 }
RESPONSE_TYPES =  { 
                    'PONG': 1, 
                    'ACK_NO_SOURCE': 2, 
                    'MESSAGE_NO_SOURCE': 3, 
                    'MESSAGE_WITH_SOURCE': 4, 
                    'ACK_WITH_SOURCE': 5
                  }

def verify_signature(event):
    raw_body = event['rawBody']
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')
    
    try:
        verify_key.verify(f'{auth_ts}{raw_body}'.encode(), bytes.fromhex(auth_sig))
    except BadSignatureError:
        raise Exception('Verification failed')

    # message = auth_ts.encode() + raw_body.encode()
    # verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    # verify_key.verify(message, bytes.fromhex(auth_sig)) # raises an error if unequal

def is_ping_pong(body):
    if body['type']:
        if body['type'] == 1:
            return True
    return False
    
def lambda_handler(event, context):
    print(f"event {event}") # debug print
    
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    # check if message is a ping
    if 'body-json' in event:
        body = event['body-json']
        if is_ping_pong(body):
            print("is_ping_pong: True")
            print(f'returning {PING_PONG}')
            return PING_PONG
        else:
            print('Found body-json, not type == 1')
            return { 'message': 'no event type' }
    elif is_ping_pong(event):
        print("is_ping_pong: True")
        print(f'returning {PING_PONG}')
        return PING_PONG
    
    # dummy return
    return {
            "type": RESPONSE_TYPES['MESSAGE_NO_SOURCE'],
            "data": {
                "tts": False,
                "content": "BEEP BOOP",
                "embeds": [],
                "allowed_mentions": []
            }
        }