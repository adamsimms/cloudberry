"""Load rig secrets from environment or a local secrets.env file (never committed)."""

from __future__ import print_function

import os

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
_DEFAULT_PATHS = (
    os.path.join(_REPO_ROOT, 'secrets.env'),
    os.path.expanduser('~/.cloudberry/secrets.env'),
)


def _load_secrets_file(path):
    if not os.path.isfile(path):
        return
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def load_secrets():
    explicit = os.environ.get('CLOUDBERRY_SECRETS_FILE')
    if explicit:
        _load_secrets_file(explicit)
    else:
        for path in _DEFAULT_PATHS:
            _load_secrets_file(path)


def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            'Missing {}. Copy .env.example to secrets.env and fill in values.'.format(name)
        )
    return value


def aws_credentials():
    load_secrets()
    return (
        require_env('AWS_ACCESS_KEY_ID'),
        require_env('AWS_SECRET_ACCESS_KEY'),
        require_env('AWS_S3_BUCKET'),
    )


def gopro_wifi_password():
    load_secrets()
    return require_env('GOPRO_WIFI_PASSWORD')
