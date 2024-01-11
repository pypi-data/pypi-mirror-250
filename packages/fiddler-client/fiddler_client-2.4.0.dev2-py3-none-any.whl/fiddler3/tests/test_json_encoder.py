from uuid import UUID

import pytest
import simplejson

from fiddler3.libs.json_encoder import RequestClientJSONEncoder


def test_json_encoder_uuid():
    data = {'uuid_field': UUID('ef3e24550e1846e0ae0e6672c3a0d5d9')}
    with pytest.raises(TypeError):
        simplejson.dumps(data)

    assert simplejson.dumps(data, cls=RequestClientJSONEncoder) == simplejson.dumps(
        {'uuid_field': 'ef3e24550e1846e0ae0e6672c3a0d5d9'}
    )
