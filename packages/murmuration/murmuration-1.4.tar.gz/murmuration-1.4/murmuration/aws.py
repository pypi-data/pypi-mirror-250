from boto3.session import Session


def kms_client(
        region: str = None,
        profile: str = None,
        *,
        role_arn: str = None,
        session: Session = None,
        client=None,):
    """
    returns a kms session
    """
    if client:
        return client
    if session:
        return session.client('kms')
    session = Session(region_name=region, profile_name=profile)
    if role_arn:
        sts = session.client('sts')
        response = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName='murmuration')
        creds = response['Credentials']
        session = Session(
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'],
        )
    return session.client('kms')
