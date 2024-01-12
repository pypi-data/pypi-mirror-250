import base64
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

import httpx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from amsdal.authentication.handlers.base import BASE_AUTH_URL
from amsdal.authentication.handlers.base import ENCRYPT_PUBLIC_KEY
from amsdal.configs.main import settings
from amsdal.errors import AmsdalDeployError


def _input(msg: str) -> str:
    return input(msg).strip()


def _print(msg: str) -> None:
    print(msg)  # noqa: T201


def want_deploy_input() -> str:
    return _input('Do you want to deploy your app? (y/N): ')


class DeployService:
    @classmethod
    def _credentials_data(cls) -> bytes:
        key = serialization.load_pem_public_key(ENCRYPT_PUBLIC_KEY.encode())
        return key.encrypt(  # type: ignore[union-attr]
            json.dumps(
                {
                    'amsdal_access_key_id': settings.ACCESS_KEY_ID,
                    'amsdal_secret_access_key': settings.SECRET_ACCESS_KEY,
                }
            ).encode('utf-8'),
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )

    @classmethod
    def deploy_prompt(cls) -> bool:
        _print('Welcome to Amsdal Framework!')
        want_to_signup = want_deploy_input()

        if want_to_signup.lower() != 'y':
            return False

        with tempfile.TemporaryDirectory() as temp_dir:
            app_dir = Path(temp_dir) / 'app'
            shutil.copytree('src', app_dir / 'src')
            shutil.copy('.amsdal-cli', app_dir / '.amsdal-cli')
            shutil.copy('requirements.txt', app_dir / 'requirements.txt')

            shutil.make_archive('app', 'zip', temp_dir)

        with open('app.zip', 'rb') as f:
            _data = base64.b64encode(f.read()).decode('utf-8')

        Path('app.zip').unlink(missing_ok=True)

        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/CreateAppDeploy/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'zip_archive': _data,
            },
            timeout=10,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Invalid credentials: {response.text}'
            raise AmsdalDeployError(msg)

        return True

    @classmethod
    def list_deploys(cls) -> list[dict[str, Any]]:
        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/ListDeploys/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
            },
            timeout=10,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Invalid credentials: {response.text}'
            raise AmsdalDeployError(msg)

        return response.json()

    @classmethod
    def update_deploy(cls, deploy_id: str) -> dict[str, Any]:
        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/CheckDeployStatus/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'deploy_id': deploy_id,
            },
            timeout=10,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Invalid credentials: {response.text}'
            raise AmsdalDeployError(msg)

        return response.json()

    @classmethod
    def destroy_deploy(cls, deploy_id: str) -> bool:
        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/DestroyAppDeploy/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'deploy_id': deploy_id,
            },
            timeout=10,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Invalid credentials: {response.text}'
            raise AmsdalDeployError(msg)

        return True
