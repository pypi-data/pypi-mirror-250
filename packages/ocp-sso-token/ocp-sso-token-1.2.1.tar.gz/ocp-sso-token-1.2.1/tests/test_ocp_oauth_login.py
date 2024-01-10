"""Test ocp_sso_token.ocp_oauth_login module."""

import unittest

import responses

from ocp_sso_token import ocp_oauth_login
from tests import helpers


class TestOcpOAuthLogin(unittest.TestCase):
    """Test OAuthLogin processing."""

    @responses.activate
    def test_flow(self) -> None:
        """Test the basic token flow."""
        helpers.setup_responses()

        login = ocp_oauth_login.OcpOAuthLogin('https://api.cluster:6443')

        self.assertEqual(login.identity_providers, {
            'Cluster-Admin': 'https://oauth-openshift.apps.cluster/oauth/authorize?'
            'client_id=openshift-browser-client&idp=Cluster-Admin&redirect_uri=https%3A%2F%2F'
            'oauth-openshift.apps.cluster%2Foauth%2Ftoken%2Fdisplay&response_type=code',
            'LDAP': 'https://oauth-openshift.apps.cluster/oauth/authorize?'
            'client_id=openshift-browser-client&idp=LDAP&redirect_uri=https%3A%2F%2F'
            'oauth-openshift.apps.cluster%2Foauth%2Ftoken%2Fdisplay&response_type=code',
            'OpenID': 'https://oauth-openshift.apps.cluster/oauth/authorize?'
            'client_id=openshift-browser-client&idp=OpenID&redirect_uri=https%3A%2F%2F'
            'oauth-openshift.apps.cluster%2Foauth%2Ftoken%2Fdisplay&response_type=code',
            'google-1': 'https://oauth-openshift.apps.cluster/oauth/authorize?'
            'client_id=openshift-browser-client&idp=google-1&redirect_uri=https%3A%2F%2F'
            'oauth-openshift.apps.cluster%2Foauth%2Ftoken%2Fdisplay&response_type=code',
        })
        self.assertEqual(login.token('OpenID'), 'sha256~code2')
        self.assertEqual(responses.calls[-1].request.body, 'code=sha256~code1&csrf=csrf1')
