import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from ldap3.core.exceptions import LDAPBindError, LDAPCertificateError, LDAPInvalidCredentialsResult, \
    LDAPInvalidServerError

from ai_arch_commons.lib.webservice_lib.core import ldap_search


class TestLdapSearch(unittest.TestCase):
    ''' Test class for src.api.core.ldap_search module '''

    def test_is_present_in_ldap_simple(self):
        ''' Test method to cover is_present_in_ldap_simple '''
        def raise_LDAPBindError(*args):
            raise LDAPBindError

        def raise_LDAPCertificateError(*args):
            raise LDAPCertificateError

        def raise_LDAPInvalidCredentialsResult(*args):
            raise LDAPInvalidCredentialsResult

        def raise_LDAPInvalidServerError(*args):
            raise LDAPInvalidServerError

        verify_username = "username"
        verify_user_password = "password"
        with \
                patch('ai_arch_commons.lib.webservice_lib.core.ldap_search.Server') as _Server, \
                patch('ai_arch_commons.lib.webservice_lib.core.ldap_search.Connection') as _Connection, \
                patch('ai_arch_commons.lib.webservice_lib.core.ldap_search.logging'):
            _search = MagicMock()
            _Connection.return_value.__enter__.return_value.search = _search
            with self.subTest():
                _search.return_value = True
                ret = ldap_search.is_present_in_ldap_simple(verify_username, verify_user_password)
                self.assertTrue(ret)
            with self.subTest():
                _search.side_effect = raise_LDAPBindError
                ret = ldap_search.is_present_in_ldap_simple(verify_username, verify_user_password)
                self.assertFalse(ret)
            with self.subTest():
                _search.side_effect = raise_LDAPCertificateError
                ret = ldap_search.is_present_in_ldap_simple(verify_username, verify_user_password)
                self.assertFalse(ret)
            with self.subTest():
                _search.side_effect = raise_LDAPInvalidCredentialsResult
                ret = ldap_search.is_present_in_ldap_simple(verify_username, verify_user_password)
                self.assertFalse(ret)
            with self.subTest():
                _search.side_effect = raise_LDAPInvalidServerError
                ret = ldap_search.is_present_in_ldap_simple(verify_username, verify_user_password)
                self.assertFalse(ret)
            _Connection.assert_any_call(_Server.return_value,
                                        user='uid=username,ou=people,dc=unicreditgroup,dc=eu',
                                        password='password',
                                        auto_bind='NO_TLS',
                                        authentication='SIMPLE')
            _search.assert_any_call('ou=groups,dc=unicreditgroup,dc=eu',
                                        '(&(cn=)(uniquemember=uid=username, ou=people, dc=unicreditgroup, dc=eu))')
            _Server.assert_any_call(host='', port=636, use_ssl=True, get_info='ALL')