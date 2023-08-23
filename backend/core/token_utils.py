from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime

def check_token_expiry(token):
    try:
        # Decode the token to access its payload
        decoded_token = AccessToken(token)
        
        # Extract the expiry time from the payload
        expiry_timestamp = decoded_token['exp']
        
        # Convert the expiry timestamp to a datetime object
        expiry_datetime = datetime.fromtimestamp(expiry_timestamp)
        
        # Check if the token has expired or not
        if expiry_datetime > datetime.now():
            print("Token is still valid. Expiry time:", expiry_datetime)
        else:
            print("Token has expired.")
            
    except Exception as e:
        print("Invalid token or unable to decode:", str(e))