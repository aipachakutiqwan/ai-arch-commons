import os
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from ai_arch_commons.lib.webservice_lib.core import security


class TestSecurity(unittest.TestCase):
    ''' Test class for src.api.core.security module '''

    def test_is_valid_credential_basic_auth(self):
        ''' Test method to cover is_valid_credential_basic_auth '''
        
        auth_username = "auth_username"
        auth_password = "auth_password"
        credential_username = "credential_username"
        credential_password = "credential_password"
        with\
                patch('ai_arch_commons.lib.webservice_lib.core.security.secrets.compare_digest') as _compare:
            _compare.side_effect = ["correct_username", "correct_password"]
            ret = security.is_valid_credential_basic_auth(auth_username, auth_password, credential_username, credential_password)
    
        self.assertEqual(ret, 'correct_password')
        _compare.assert_any_call(credential_username, auth_username)
        _compare.assert_any_call(credential_password, auth_password)

    def test_clear_cache_credential(self):
        ''' Test method to cover clear_cache_credential '''
        arg_cache_credential = {"auth_username": {"creation_time": 1}}
        auth_username = "auth_username"
        arg_cleanup_interval_cache_credential = 0
        with\
                patch('ai_arch_commons.lib.webservice_lib.core.security.datetime.date') as _date,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.datetime.datetime') as _datetime:
            _datetime.combine.return_value.total_seconds.return_value = 1
            _datetime.combine.return_value.__sub__.return_value = _datetime.combine.return_value
            security.clear_cache_credential(arg_cache_credential, auth_username, arg_cleanup_interval_cache_credential)
        _date.assert_any_call(1, 1, 1)
        _datetime.combine.assert_any_call(_date.return_value, 1)
        _datetime.combine.assert_any_call(_date.return_value, _datetime.now.return_value.time.return_value)
        _datetime.now.assert_called()
        _datetime.combine.return_value.total_seconds.assert_called()

    def test_ldap_verification(self):
        ''' Test method to cover ldap_verification '''
        verify_username = "username"
        verify_user_password = "password"
        with\
                patch('ai_arch_commons.lib.webservice_lib.core.security.is_present_in_ldap_simple') as _is_present,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.datetime.datetime') as _datetime:
            _is_present.return_value = True
            ret = security.ldap_verification(verify_username, verify_user_password)
        self.assertEqual(ret, ("username", "password"))
        _datetime.now.assert_called()
        _datetime.now.return_value.time.assert_called()
        _is_present.assert_any_call(verify_username='username', verify_user_password='password')

    def test_verify_in_ldap(self):
        ''' Test method to cover verify_in_ldap '''
        flag_cache_credential = True
        auth_username = "username"
        credentials = MagicMock()
        credentials.username = "username"
        credentials.password = "password"
        with\
                patch('ai_arch_commons.lib.webservice_lib.core.security.ldap_verification') as _ldap_verification,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.CACHE_CREDENTIAL') as _CACHE_CREDENTIAL,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.raise_basic_auth_exception') as _raise,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.is_valid_credential_basic_auth') as _is_valid:
            _ldap_verification.return_value = ("username", "password")
            _is_valid.return_value = False
            ret = security.verify_in_ldap(flag_cache_credential, auth_username, credentials)

        self.assertFalse(ret)
        _is_valid.assert_any_call(auth_username='username', auth_password='password', credential_username='username',
                                  credential_password='password')
        _ldap_verification.assert_any_call(verify_username='username', verify_user_password='password')
        _raise.assert_any_call(details='Incorrect username or password.')

    def test_is_authenticated(self):
        ''' Test method to cover is_authenticated '''
        os.environ["DISABLE_AUTH"] = "false"
        credentials = MagicMock()
        credentials.username = "username"
        credentials.password = "password"
        with\
                patch('ai_arch_commons.lib.webservice_lib.core.security.Depends') as _Depends,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.clear_cache_credential') as _clear_credential,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.is_valid_credential_basic_auth') as _is_valid,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.verify_in_ldap') as _verify,\
                patch('ai_arch_commons.lib.webservice_lib.core.security.ldap_verification') as _ldap:
            security.CACHE_CREDENTIAL = {"username": {"auth_password": "password"}}

            ret = security.is_authenticated(credentials)

        self.assertTrue(ret)
        _clear_credential.assert_any_call({'username': {'auth_password': 'password'}}, 'username', 3600)
        _is_valid.assert_any_call(auth_username='username', auth_password='password', credential_username='username',
                                  credential_password='password')
