import boto3
import json
from config.settings import Config

def get_secret(secret_name=None):
    if not secret_name:
        secret_name = Config.SECRET_NAME
        
    client = boto3.client(
        'secretsmanager',
        region_name=Config.AWS_REGION
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error obteniendo secreto: {str(e)}")
        return {}