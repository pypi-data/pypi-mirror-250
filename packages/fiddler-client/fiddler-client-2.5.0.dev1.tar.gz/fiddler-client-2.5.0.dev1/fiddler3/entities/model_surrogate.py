from __future__ import annotations

from typing import Any, Callable
from uuid import UUID

from fiddler3.decorators import handle_api_error
from fiddler3.entities.job import Job
from fiddler3.schemas.deployment_params import ArtifactType, DeploymentParams
from fiddler3.schemas.job import JobCompactResp
from fiddler3.utils.logger import get_logger

logger = get_logger(__name__)


class SurrogateMixin:
    id: UUID | None
    _client: Callable

    def _check_id_attributes(self) -> None:
        if not self.id:
            raise AttributeError(
                'This method is available only for model object generated from '
                'API response.'
            )

    def _deploy_surrogate_model(
        self,
        deployment_params: DeploymentParams | None = None,
        update: bool = False,
    ) -> Job:
        """
        Add surrogate model to an existing model

        :param deployment_params: Model deployment parameters
        :param update: Set True for re-generating surrogate model, otherwise False
        :return: Async job uuid
        """
        payload: dict[str, Any] = {}

        if deployment_params:
            deployment_params.artifact_type = ArtifactType.SURROGATE
            payload.update(
                {'deployment_params': deployment_params.dict(exclude_unset=True)}
            )

        url = f'/v3/models/{self.id}/deploy-surrogate'
        method: Callable = self._client().put if update else self._client().post
        response = method(url=url, data=payload)

        job_compact = JobCompactResp(**response.json()['data']['job'])

        logger.info(
            'Model[%s] - Submitted job (%s) for deploying a surrogate model',
            self.id,
            job_compact.id,
        )

        return Job.get(id_=job_compact.id)

    @handle_api_error
    def add_surrogate(
        self,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Add a new surrogate.

        :param deployment_params: Model deployment parameters
        :return: Async job.
        """
        self._check_id_attributes()
        job = self._deploy_surrogate_model(
            deployment_params=deployment_params, update=False
        )
        return job

    @handle_api_error
    def update_surrogate(
        self,
        deployment_params: DeploymentParams | None = None,
    ) -> Job:
        """
        Update an existing surrogate.

        :param deployment_params: Model deployment parameters
        :return: Async job.
        """
        self._check_id_attributes()
        job = self._deploy_surrogate_model(
            deployment_params=deployment_params, update=True
        )
        return job
