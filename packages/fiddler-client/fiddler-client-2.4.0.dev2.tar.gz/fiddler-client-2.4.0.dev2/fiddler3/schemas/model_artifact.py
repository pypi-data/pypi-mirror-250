from fiddler3.schemas.base import BaseModel


class ModelArtifactDeployMultiPartUploadResp(BaseModel):
    part_number: int
    etag: str
