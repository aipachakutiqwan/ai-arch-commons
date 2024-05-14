"""
Search credentials in LDAP
"""

import logging
import os
from ldap3 import Server, Connection, ALL, AUTO_BIND_NO_TLS
from ldap3.core.exceptions import LDAPBindError, LDAPCertificateError, \
    LDAPInvalidCredentialsResult, LDAPInvalidServerError

LDAP_SERVER_NAME = os.environ.get("LDAP_SERVER_NAME", "")
SEARCH_QUERY_CN = os.environ.get("SEARCH_QUERY_CN", "")


def is_present_in_ldap_simple(verify_username, verify_user_password):
    """
    Validate username and password in LDAP
    Args:
        :param  verify_username: verify_username
        :param  verify_user_password: verify_user_password
    Returns:
        boolean: If credentials match in LDAP
    """
    ldap_search_flag = False
    ldap_server_name = LDAP_SERVER_NAME
    port = 636
    try:
        logging.info(f"Connecting LDAP: {LDAP_SERVER_NAME} group: "
                     f"{SEARCH_QUERY_CN} user: {verify_username}")
        server = Server(host=ldap_server_name, port=port, use_ssl=True, get_info=ALL)
        bind_dn = f'uid={verify_username},ou=people,dc=unicreditgroup,dc=eu'
        search_base = 'ou=groups,dc=unicreditgroup,dc=eu'
        search_query = f'(&(cn={SEARCH_QUERY_CN})(uniquemember=uid={verify_username}, ' \
                       f'ou=people, dc=unicreditgroup, dc=eu))'
        with Connection(server, user=bind_dn,
                        password=verify_user_password,
                        auto_bind=AUTO_BIND_NO_TLS,
                        authentication='SIMPLE') as conn:
            ldap_search_flag = conn.search(search_base, search_query)
            logging.info(f"LDAP search results: {ldap_search_flag}")
    except LDAPBindError:
        logging.exception('LDAP bind error.')
    except LDAPCertificateError:
        logging.exception('LDAP certificate error.')
    except LDAPInvalidCredentialsResult:
        logging.exception(f'Invalid base user: {verify_username}.')
    except LDAPInvalidServerError:
        logging.exception(f'Invalid server: {ldap_server_name}.')
    return ldap_search_flag
