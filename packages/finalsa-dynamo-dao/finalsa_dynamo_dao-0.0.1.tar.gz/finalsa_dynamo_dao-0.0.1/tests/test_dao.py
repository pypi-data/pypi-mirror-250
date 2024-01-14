import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from finalsa_dynamo_dao.dao import BaseDao


class UserBaseDao(BaseDao): 
    PK:str = "test"
    SK:str = "test"
    


def test_pk():
    dao = UserBaseDao(
        PK="test",
        SK="test"
    )
    assert dao.PK == "test"

    d = dao.dict()

    assert d['PK'] == {"S": "test"}