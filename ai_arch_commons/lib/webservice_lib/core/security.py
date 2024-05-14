"""
LDAP validation functions
"""
import datetime
import logging
import os
import secrets
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from ai_arch_commons.lib.webservice_lib.core.ldap_search import is_present_in_ldap_simple

http_basic_security_obj = HTTPBasic()
LDAP_SEARCH = os.environ.get("LDAP_SEARCH_FLAG", True)
CACHE_CREDENTIAL = {}
# We are using a cache credential interval of 3600 sec = 1 hour
CLEANUP_INTERVAL_CACHE_CREDENTIAL = os.environ.get("cleanup_interval_cache_credential", 3600)


def is_valid_credential_basic_auth(auth_username, auth_password,
                                   credential_username, credential_password):
    """
    Validate credentials username and password
    Args:
        :param  auth_username: auth_username
        :param  auth_password: auth_password
        :param  credential_username: credential_username
        :param  credential_password: credential_password
    Returns:
        boolean: True/False
    """
    correct_username = False
    correct_password = False

    if auth_username is not None and auth_password is not None \
            and credential_username is not None and \
            credential_password is not None:
        correct_username = secrets.compare_digest(credential_username, auth_username)
        correct_password = secrets.compare_digest(credential_password, auth_password)

    return correct_username and correct_password


def clear_cache_credential(arg_cache_credential, auth_username,
                           arg_cleanup_interval_cache_credential):
    """
    Clear cache if it is more than 3600 sec
    Args:
        :param  arg_cache_credential: dict containing password for user
        :param  auth_username: auth_username
        :param  arg_cleanup_interval_cache_credential: cache credential interval of 3600 sec
    Returns:
        Cleared cache if time exceeded
    """
    credential_creation_time = arg_cache_credential.get(auth_username, {}). \
        get('creation_time', None)
    if credential_creation_time is not None:
        current_time = datetime.datetime.now().time()
        date = datetime.date(1, 1, 1)
        start_time_converted = datetime.datetime.combine(date, credential_creation_time)
        end_time_converted = datetime.datetime.combine(date, current_time)
        time_elapsed = end_time_converted - start_time_converted
        if time_elapsed.total_seconds() > arg_cleanup_interval_cache_credential:
            del arg_cache_credential[auth_username]


def ldap_verification(verify_username, verify_user_password):
    """
    Validate credentials username and password in LDAP
    Args:
        :param  verify_username: verify_username
        :param  verify_user_password: verify_user_password
    Returns:
        auth_username: auth_username
        auth_password: auth_password
    """
    global CACHE_CREDENTIAL
    auth_username = None
    auth_password = None
    if is_present_in_ldap_simple(verify_username=verify_username,
                                 verify_user_password=verify_user_password):
        auth_username = verify_username
        auth_password = verify_user_password
        CACHE_CREDENTIAL[auth_username] = {
            'auth_password': auth_password,
            'creation_time': datetime.datetime.now().time()
        }
    else:
        raise_basic_auth_exception(details=f"Username={verify_username} not present in LDAP group.")
    return auth_username, auth_password


def raise_basic_auth_exception(details):
    """
    Raise basic auth error
    Args:
        :param  details: text description
    Returns:
        HTTPException: HTTPException
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=details,
        headers={"WWW-Authenticate": "Basic"},
    )


def verify_in_ldap(flag_cache_credential, auth_username, credentials):
    """
    Validate credentials username and password in LDAP
    Args:
        :param  flag_cache_credential: flag_cache_credential
        :param  auth_username: auth_username
        :param  credentials: HTTPBasicCredentials(username, password)
    Returns:
        boolean: If credentials was verified in LDAP
    """
    # We will again try with ldap search in case of the cache credential based condition
    # We will invalidate i.e. empty the cache_credential
    if flag_cache_credential:
        if auth_username in CACHE_CREDENTIAL:
            del CACHE_CREDENTIAL[auth_username]
        auth_username, auth_password = ldap_verification(verify_username=credentials.username,
                                                         verify_user_password=credentials.password)

        if not is_valid_credential_basic_auth(auth_username=auth_username,
                                              auth_password=auth_password,
                                              credential_username=credentials.username,
                                              credential_password=credentials.password):
            if auth_username in CACHE_CREDENTIAL:
                del CACHE_CREDENTIAL[auth_username]
            raise_basic_auth_exception(details="Incorrect username or password.")
            return False
    else:
        raise_basic_auth_exception(details="Incorrect username or password.")
        return False


def is_authenticated(credentials: HTTPBasicCredentials = Depends(http_basic_security_obj)):
    """
    If LDAP is enabled
      > the first time we should use it to validate user credentials (user, pass)
      > the second time we should use the cached validated credentials to authenticate the request
      > The cache should have an expiration (configurable)
      > If the cache is expired we recheck LDAP
    If LDAP disabled
      > Fall back to old usage by environment variables digest comparison
    """
    global CACHE_CREDENTIAL
    global CLEANUP_INTERVAL_CACHE_CREDENTIAL

    if os.environ.get("DISABLE_AUTH", False) in [True, 'true', 'True']:
        return True

    flag_cache_credential = False

    if LDAP_SEARCH in [True, 'true', 'True']:
        if CACHE_CREDENTIAL:
            auth_username = credentials.username
            auth_password = CACHE_CREDENTIAL.get(auth_username, {}).get('auth_password', None)
            flag_cache_credential = True
            logging.debug(f'User: {auth_username} found in cache.')
        else:
            logging.info(f'User: {credentials.username}/{credentials.password} is going to the ldap verification.')
            # Check in ldap using ldap_search
            auth_username, auth_password =\
                ldap_verification(verify_username=credentials.username,
                                  verify_user_password=credentials.password)
    else:
        auth_username = os.environ.get("auth_username")
        auth_password = os.environ.get("auth_password")

    if not is_valid_credential_basic_auth(auth_username=auth_username, auth_password=auth_password,
                                          credential_username=credentials.username,
                                          credential_password=credentials.password):
        return verify_in_ldap(flag_cache_credential, auth_username, credentials)
    clear_cache_credential(CACHE_CREDENTIAL, auth_username, CLEANUP_INTERVAL_CACHE_CREDENTIAL)
    logging.debug(f'Ldap search complete for the user: {credentials.username}.')
    return True
