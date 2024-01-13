from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

CustomFeatureTypeVar = TypeVar('CustomFeatureTypeVar', bound='CustomFeature')
DEFAULT_NUM_CLUSTERS = 5
DEFAULT_NUM_TAGS = 5


class CustomFeatureType(str, Enum):
    FROM_COLUMNS = 'FROM_COLUMNS'
    FROM_VECTOR = 'FROM_VECTOR'
    FROM_TEXT_EMBEDDING = 'FROM_TEXT_EMBEDDING'
    FROM_IMAGE_EMBEDDING = 'FROM_IMAGE_EMBEDDING'
    ENRICHMENT = 'ENRICHMENT'


class CustomFeature(BaseModel):
    name: str
    type: CustomFeatureType
    n_clusters: Optional[int] = DEFAULT_NUM_CLUSTERS
    centroids: Optional[List] = None

    class Config:
        allow_mutation = False

    @classmethod
    def from_columns(
        cls, custom_name: str, cols: List[str], n_clusters: int = DEFAULT_NUM_CLUSTERS
    ) -> 'Multivariate':
        return Multivariate(
            name=custom_name,
            columns=cols,
            n_clusters=n_clusters,
        )

    @classmethod
    def from_dict(cls: Type[CustomFeatureTypeVar], deserialized_json: dict) -> Any:
        feature_type = CustomFeatureType(deserialized_json['type'])
        if feature_type == CustomFeatureType.FROM_COLUMNS:
            return Multivariate.parse_obj(deserialized_json)
        if feature_type == CustomFeatureType.FROM_VECTOR:
            return VectorFeature.parse_obj(deserialized_json)
        if feature_type == CustomFeatureType.FROM_TEXT_EMBEDDING:
            return TextEmbedding.parse_obj(deserialized_json)
        if feature_type == CustomFeatureType.FROM_IMAGE_EMBEDDING:
            return ImageEmbedding.parse_obj(deserialized_json)
        if feature_type == CustomFeatureType.ENRICHMENT:
            return Enrichment.parse_obj(deserialized_json)

        raise ValueError(f'Unsupported feature type: {feature_type}')

    def to_dict(self) -> Dict[str, Any]:
        return_dict: Dict[str, Any] = {
            'name': self.name,
            'type': self.type.value,
            'n_clusters': self.n_clusters,
        }
        if isinstance(self, Multivariate):
            return_dict['columns'] = self.columns
        elif isinstance(self, VectorFeature):
            return_dict['column'] = self.column
            if isinstance(self, (ImageEmbedding, TextEmbedding)):
                return_dict['source_column'] = self.source_column
                if isinstance(self, TextEmbedding):
                    return_dict['n_tags'] = self.n_tags
        elif isinstance(self, Enrichment):
            return_dict['columns'] = self.columns
            return_dict['enrichment'] = self.enrichment
            return_dict['config'] = self.config
        else:
            raise ValueError(f'Unsupported feature type: {self.type} {type(self)}')

        return return_dict


class Multivariate(CustomFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_COLUMNS
    columns: List[str]
    monitor_components: bool = False


class VectorFeature(CustomFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_VECTOR
    source_column: Optional[str] = None
    column: str


class TextEmbedding(VectorFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_TEXT_EMBEDDING
    n_tags: Optional[int] = DEFAULT_NUM_TAGS


class ImageEmbedding(VectorFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_IMAGE_EMBEDDING


class Enrichment(CustomFeature):
    """
    Represents an enrichment feature in a data processing or machine learning context.

    This class inherits from CustomFeature and is used to apply specific enrichment
    operations to a set of columns in a dataset. The type of enrichment and its
    configuration can be specified.

    Attributes:
        type (CustomFeatureType): The type of the custom feature, set to ENRICHMENT.
        columns (List[str]): The list of input column names in the dataset used to generate the enrichment.
        enrichment (str): A string identifier for the type of enrichment to be applied.
        config (Dict[str, Any]): A dictionary containing configuration options for the enrichment.
    """

    # Setting the feature type to ENRICHMENT
    type: CustomFeatureType = CustomFeatureType.ENRICHMENT

    # List of input column names used to generate the enrichment
    columns: List[str]

    # String identifier for the enrichment to be applied. e.g. "embedding" or "toxicity"
    enrichment: str

    # Dictionary for additional configuration options for the enrichment
    config: Dict[str, Any] = {}
