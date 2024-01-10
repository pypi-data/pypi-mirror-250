from boto3.session import Session
from .helpers import as_bytes
from .helpers import b64_str
from .helpers import from_b64_str
from .aws import kms_client
from .helpers import prefix_alias


def encrypt_bytes(
        plain_text: bytes,
        alias: str,
        region: str = None,
        profile: str = None,
        role_arn: str = None,
        session: Session = None,
        client=None) -> bytes:
    client = kms_client(
        region, profile, role_arn=role_arn,
        session=session, client=client)
    alias = prefix_alias(alias)
    data = client.encrypt(KeyId=alias, Plaintext=plain_text)
    return data['CiphertextBlob']


def decrypt_bytes(
        cipher_text: bytes,
        region: str = None,
        profile: str = None,
        role_arn: str = None,
        session: Session = None,
        client=None) -> bytes:
    client = kms_client(
        region, profile, role_arn=role_arn,
        session=session, client=client)
    data = client.decrypt(CiphertextBlob=cipher_text)
    return data['Plaintext']


def encrypt(
        plain_text,
        alias,
        region: str = None,
        profile: str = None,
        role_arn: str = None,
        session: Session = None,
        client=None) -> str:
    plain_text = as_bytes(plain_text)
    data = encrypt_bytes(
        plain_text, alias, region, profile,
        role_arn=role_arn, session=session, client=client)
    return b64_str(data)


def decrypt(
        cipher_text: str,
        region: str = None,
        profile: str = None,
        role_arn: str = None,
        session: Session = None,
        client=None,):
    cipher_text = from_b64_str(cipher_text)
    data = decrypt_bytes(
        cipher_text, region, profile, role_arn=role_arn,
        session=session, client=client)
    return data.decode('utf-8')
