"""Test ocp_sso_token.__main__ module."""
import contextlib
import io
import os
import pathlib
import tempfile
import typing
import unittest
from unittest import mock

import responses
import yaml

from ocp_sso_token import __main__
from tests import helpers


class TestMain(unittest.TestCase):
    """Test ocp_sso_token.__main__ module."""

    @responses.activate
    def test_main(self) -> None:
        """Test the main method."""
        helpers.setup_responses()

        cases: typing.Iterable[
            typing.Tuple[typing.List[str], str, typing.Optional[Exception], typing.Any]
        ] = (
            (['https://api.cluster:6443'],
             'sha256~code2', None, None),
            (['https://api.cluster:6443', '--identity-providers', 'foo'],
             '', Exception('find OpenID'), None),
            (['https://api.cluster:6443', '--context', 'context', '--namespace', 'namespace'],
             '', None, {
                "apiVersion": "v1", "kind": "Config",
                'clusters': [{
                    'name': 'api-cluster:6443',
                    'cluster': {'server': 'https://api.cluster:6443'},
                }],
                'users': [{
                    'name': 'api-cluster:6443',
                    'user': {'token': 'sha256~code2'}
                }],
                'contexts': [{
                    'name': 'context',
                    'context': {'cluster': 'api-cluster:6443',
                                'user': 'api-cluster:6443',
                                'namespace': 'namespace'},
                }],
            }),
        )
        for args, output, exception, config in cases:
            with self.subTest(args=args), tempfile.TemporaryDirectory() as tempdir:
                tempconf = pathlib.Path(tempdir, 'conf')
                raises = (self.assertRaisesRegex(Exception, str(exception))
                          if isinstance(exception, Exception) else contextlib.nullcontext())
                with mock.patch.dict(os.environ, {'KUBECONFIG': str(tempconf)}), \
                        contextlib.redirect_stdout(stdout := io.StringIO()), \
                        raises:
                    __main__.main(args)
                self.assertEqual(stdout.getvalue().strip(), output)
                if config:
                    self.assertEqual(yaml.safe_load(tempconf.read_text(encoding='utf8')), config)
