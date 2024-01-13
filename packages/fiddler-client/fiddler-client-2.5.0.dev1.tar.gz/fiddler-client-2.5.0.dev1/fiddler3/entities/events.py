from __future__ import annotations

from pathlib import Path
from typing import Any, Callable
from uuid import UUID

import pandas as pd
from requests import Response

from fiddler3.decorators import handle_api_error
from fiddler3.entities.files import File
from fiddler3.entities.job import Job
from fiddler3.schemas.dataset import EnvType
from fiddler3.schemas.events import EventsSource, FileSource
from fiddler3.schemas.job import JobCompactResp

STREAM_EVENTS_MAX = 1000


class EventMixin:
    id: UUID | None
    _client: Callable

    @handle_api_error
    def publish(
        self,
        source: list[dict[Any, Any]] | str | Path | pd.DataFrame,
        environment: EnvType,
        dataset_name: str | None = None,
    ) -> list[UUID] | Job:
        """
        Publish Pre-production or Production data

        :param source: source can be:
            Path or str path: path for data file.
            list[dict]: list of event dicts. max_len=1000. EnvType.PRE_PRODUCTION not supported
            dataframe: events dataframe. EnvType.PRE_PRODUCTION not supported.
        :param environment: either EnvType.PRE_PRODUCTION or EnvType.PRODUCTION
        :param dataset_name: name of the dataset. Not supported for EnvType.PRODUCTION

        :return: list[UUID] for list of dicts or dataframe source and Job object for file path source.
        """
        _sources = self._get_sources(source)
        if isinstance(_sources, FileSource):
            return self._publish_file(
                source=_sources,
                environment=environment,
                dataset_name=dataset_name,
            )
        return self._publish_stream(
            sources=_sources,
            environment=environment,
            dataset_name=dataset_name,
        )

    def _publish_stream(
        self,
        sources: list[EventsSource],
        environment: EnvType,
        dataset_name: str | None = None,
    ) -> list[UUID]:
        fiddler_ids = []
        for _source in sources:
            response = self._publish_call(
                source=_source,
                environment=environment,
                dataset_name=dataset_name,
            )
            fiddler_ids.extend(response.json()['data']['fiddler_ids'])

        return fiddler_ids

    def _publish_file(
        self,
        source: FileSource,
        environment: EnvType,
        dataset_name: str | None = None,
    ) -> Job:
        response = self._publish_call(
            source=source, environment=environment, dataset_name=dataset_name
        )
        job_compact = JobCompactResp(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)

    def _get_sources(
        self, source: list[dict[str, Any]] | str | Path | pd.DataFrame
    ) -> list[EventsSource] | FileSource:
        _source = []
        if isinstance(source, (str, Path)):
            file = File(path=Path(source)).upload()
            assert file.id is not None
            return FileSource(file_id=file.id)

        if isinstance(source, list):
            _source.append(EventsSource(events=source))

        elif isinstance(source, pd.DataFrame):
            for event_dict in [
                source[i : i + STREAM_EVENTS_MAX]
                for i in range(0, source.shape[0], STREAM_EVENTS_MAX)
            ]:
                _source.append(EventsSource(events=event_dict.to_dict('records')))

        return _source

    def _publish_call(
        self,
        source: FileSource | EventsSource,
        environment: EnvType,
        dataset_name: str | None = None,
    ) -> Response:
        return self._client().post(
            url='/v3/events',
            data={
                'source': source.dict(),
                'model_id': self.id,
                'env_type': environment,
                'env_name': dataset_name,
            },
        )
