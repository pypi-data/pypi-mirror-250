"""
Utilities to control permission grants for AWS roles.

"""
import asyncio
import datetime

import aioboto3

from lassen.core.config import get_settings

global_session = None
session_expiration = None
session_lock = asyncio.Lock()


async def is_session_valid(expiration):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    return expiration is not None and current_time < expiration - datetime.timedelta(
        minutes=5
    )


async def assume_aws_credentials():
    """
    Assumes specific credentials given the default assumable role in the settings.
    By convention, we assume that backend services will only want one valid sessions
    to AWS at a time. We cache it globally until expiration to save us from having
    to do the round-trip of reauthentication on each request.

    """
    global global_session, session_expiration

    # First, non-blocking check for session validity
    if await is_session_valid(session_expiration):
        return global_session

    async with session_lock:
        # Re-check the session validity in case it got updated while
        # waiting for the lock
        if await is_session_valid(session_expiration):
            return global_session

        settings = get_settings()

        session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

        async with session.client("sts") as sts_client:
            assumed_role = await sts_client.assume_role(
                RoleArn=settings.AWS_ROLE_ARN,
                RoleSessionName=settings.AWS_ROLE_SESSION_NAME,
            )

        session_expiration = datetime.datetime.fromtimestamp(
            assumed_role["Credentials"]["Expiration"].timestamp(), datetime.timezone.utc
        )

        global_session = aioboto3.Session(
            aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role["Credentials"]["SecretAccessKey"],
            aws_session_token=assumed_role["Credentials"]["SessionToken"],
            region_name=settings.AWS_REGION_NAME,
        )

        return global_session
