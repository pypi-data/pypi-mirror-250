from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


def clean_list(items: list):
    result = []
    for v in items:
        if not v:
            continue
        result.append(v)
    return result


def parse_dao_to_dict(v):
    if isinstance(v, BaseDao):
        return None
    elif isinstance(v, list):
        helper = clean_list([parse_dao_to_dict(v) for v in v])
        if len(helper) == 0:
            return None
        return helper
    else:
        return v


def is_valid_property(k: str):
    if k.startswith('_'):
        return False
    if k == 'id':
        return False
    return True


def translate_model_to_dynamo_model(dict: dict):
    serializer = TypeSerializer()

    def to_supported_type(v):
        if isinstance(v, datetime):
            return v.isoformat()
        if isinstance(v, float):
            return Decimal(v)
        if isinstance(v, date):
            return v.isoformat()
        if isinstance(v, UUID):
            return str(v)
        return v
    return {k: serializer.serialize(to_supported_type(v)) for k, v in dict.items()}


def tranlate_dynamo_model_to_model(dict: dict):
    serializer = TypeDeserializer()
    return {k: serializer.deserialize(v) for k, v in dict.items()}


class BaseDao():

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dict(self):
        result_items = {}
        for k, v in self.__dict__.items():
            if not is_valid_property(k):
                continue
            value = parse_dao_to_dict(v)
            if value is None:
                continue
            result_items[k] = value
        r = translate_model_to_dynamo_model(result_items)
        return r

    def reverse(self, ):
        d = self.dict()
        sk = d['SK']
        d['SK'] = d['PK']
        d['PK'] = sk
        return d

    @classmethod
    def from_dynamo_model(cls, dict: dict, **kwargs):
        d = tranlate_dynamo_model_to_model(dict)
        d = {**d, **kwargs}
        return cls(**d)

    def __str__(self) -> str:
        return str(self.dict())
