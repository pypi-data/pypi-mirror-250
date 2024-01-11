from __future__ import annotations

import json
import math
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Callable
from uuid import UUID

from fiddler3.constants.common import (
    CONTENT_TYPE_OCTET_STREAM_HEADER,
    MULTI_PART_CHUNK_SIZE,
)
from fiddler3.decorators import handle_api_error
from fiddler3.entities.job import Job
from fiddler3.schemas.deployment_params import ArtifactType, DeploymentParams
from fiddler3.schemas.job import JobCompactResp
from fiddler3.schemas.model_artifact import ModelArtifactDeployMultiPartUploadResp
from fiddler3.utils.logger import get_logger
from fiddler3.utils.validations import validate_artifact_dir

logger = get_logger(__name__)


class ArtifactMixin:
    id: UUID | None
    _client: Callable

    def _get_method(self, update: bool = False) -> Callable:
        """Get HTTP method"""
        return self._client().put if update else self._client().post

    def _deploy_model_artifact(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """
        Upload and deploy model artifact for an existing model

        :param model_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param update: Set True for updating artifact, False for adding artifact
        :return: Async job
        """
        model_dir = Path(model_dir)
        validate_artifact_dir(model_dir)

        if (
            deployment_params
            and deployment_params.artifact_type.upper() == ArtifactType.SURROGATE
        ):
            raise ValueError(
                f'{ArtifactType.SURROGATE} artifact_type is an invalid value for this '
                f'method. Use {ArtifactType.PYTHON_PACKAGE} instead.'
            )

        with tempfile.TemporaryDirectory() as tmp:
            # Archive model artifact directory
            logger.info(
                'Model[%s] - Tarring model artifact directory - %s',
                self.id,
                model_dir,
            )
            file_path = shutil.make_archive(
                base_name=str(Path(tmp) / 'files'),
                format='tar',
                root_dir=str(model_dir),
                base_dir='.',
            )

            logger.info(
                'Model[%s] - Model artifact tar file created at %s',
                self.id,
                file_path,
            )

            # Choose deployer based on archive file size
            if os.path.getsize(file_path) < MULTI_PART_CHUNK_SIZE:
                job = self._artifact_deploy(
                    file_path=Path(file_path),
                    deployment_params=deployment_params,
                    update=update,
                )
            else:
                job = self._artifact_deploy_multipart(
                    file_path=Path(file_path),
                    deployment_params=deployment_params,
                    update=update,
                )

        logger.info(
            'Model[%s] - Submitted job (%s) for deploying model artifact',
            self.id,
            job.id,
        )

        return job

    def _initialize_multi_part_upload(self, update: bool = False) -> str:
        """
        Initialize multi-part upload request

        :return: Multi-part upload id
        """
        logger.info(
            'Model[%s] - Initializing multi-part model upload',
            self.id,
        )

        method = self._get_method(update)

        response = method(url=f'/v3/models/{self.id}/deploy-artifact-multi-part-init')

        response_data = response.json().get('data', {})

        logger.info(
            'Model[%s] - Multi-part model upload initialized',
            self.id,
        )
        return response_data.get('upload_id', '')

    def _upload_multi_part_chunk(
        self, data: bytes, upload_id: str, part_number: int, update: bool
    ) -> dict:
        """
        Upload data chunk

        :param data: Data chunk
        :param upload_id: Multi-part upload id
        :param part_number: Chunk part number
        :return: Part details
        """
        method = self._get_method(update)

        response = method(
            url=f'/v3/models/{self.id}/deploy-artifact-multi-part-upload',
            params={
                'upload_id': upload_id,
                'part_number': part_number,
            },
            data=data,
            headers=CONTENT_TYPE_OCTET_STREAM_HEADER,
        )
        response_data = ModelArtifactDeployMultiPartUploadResp(
            **response.json()['data']
        )

        return {
            'etag': response_data.etag,
            'part_number': response_data.part_number,
        }

    def _complete_multi_part_upload(
        self,
        upload_id: str,
        parts: list[dict],
        update: bool,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Complete multi-part upload request and deploy model artifact

        :param upload_id: Multi-part upload id
        :param parts: List of all parts
        :param deployment_params: Deployment parameters
        :return: Async job
        """
        method = self._get_method(update)
        payload: dict[str, Any] = {
            'upload_id': upload_id,
            'parts': parts,
        }

        if deployment_params:
            payload['deployment_params'] = deployment_params.dict(exclude_unset=True)

        response = method(
            url=f'/v3/models/{self.id}/deploy-artifact-multi-part-complete',
            data=payload,
        )

        logger.info(
            'Model[%s] - Multi-part model upload completed',
            self.id,
        )
        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    def _artifact_deploy_multipart(
        self,
        file_path: Path,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """
        Upload and deploy model artifact

        :param file_path: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :param update: Flag for add or update artifacts
        :return: Async job uuid
        """
        # 1. Initialize multi-part upload request
        upload_id = self._initialize_multi_part_upload(update)
        part_number = 1
        parts = []
        file_size = os.path.getsize(file_path)
        total_chunks = math.ceil(file_size / MULTI_PART_CHUNK_SIZE)

        # 2. Chunk and upload
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(MULTI_PART_CHUNK_SIZE)
                if not data:
                    break

                logger.info(
                    'Model[%s] - Uploading multi-part chunk - %d/%d',
                    self.id,
                    part_number,
                    total_chunks,
                )

                part = self._upload_multi_part_chunk(
                    data=data,
                    upload_id=upload_id,
                    part_number=part_number,
                    update=update,
                )
                parts.append(part)
                logger.info(
                    'Model[%s] - Uploaded multi-part chunk - %d/%d',
                    self.id,
                    part_number,
                    total_chunks,
                )
                part_number += 1

        # 3: Complete the upload
        return self._complete_multi_part_upload(
            upload_id=upload_id,
            parts=parts,
            update=update,
            deployment_params=deployment_params,
        )

    def _artifact_deploy(
        self,
        file_path: Path,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """Artifact deploy base method."""
        method = self._get_method(update)
        params = {}
        if deployment_params:
            params['deployment_params'] = json.dumps(
                deployment_params.dict(exclude_unset=True)
            )

        with open(file_path, 'rb') as f:
            data = f.read()
            response = method(
                url=f'/v3/models/{self.id}/deploy-artifact',
                params=params,
                data=data,
                headers=CONTENT_TYPE_OCTET_STREAM_HEADER,
            )

        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    @handle_api_error
    def add_artifact(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Upload and deploy model artifact.

        :param model_dir: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job.
        """
        self._check_id_attributes()
        job = self._deploy_model_artifact(
            model_dir=model_dir, deployment_params=deployment_params
        )
        return job

    @handle_api_error
    def update_artifact(
        self,
        model_dir: str | Path,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Update existing model artifact.

        :param model_dir: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job.
        """
        self._check_id_attributes()
        job = self._deploy_model_artifact(
            model_dir=model_dir, deployment_params=deployment_params, update=True
        )
        return job

    @handle_api_error
    def download_artifact(
        self,
        output_dir: str | Path,
    ) -> None:
        """
        Download existing model artifact.

        :param output_dir: Path to download model artifact tar file
        """
        self._check_id_attributes()
        output_dir = Path(output_dir)
        if output_dir.exists():
            raise ValueError(f'Output dir already exists {output_dir}')

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Download tar file
            tar_file_path = os.path.join(tmp_dir, 'artifact.tar')

            with self._client().get(
                url=f'/v3/models/{self.id}/download-artifact'
            ) as resp:
                resp.raise_for_status()
                with open(tar_file_path, mode='wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            os.makedirs(output_dir, exist_ok=True)
            shutil.unpack_archive(tar_file_path, extract_dir=output_dir, format='tar')

    def _check_id_attributes(self) -> None:
        if not self.id:
            raise AttributeError(
                'This method is available only for model object generated from '
                'API response.'
            )
