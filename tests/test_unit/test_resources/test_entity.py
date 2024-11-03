from src.fastddd.resources import entity
from pydantic import BaseModel

from src.fastddd.errors.app import ValidationException


@entity()
class Entity1Test(BaseModel):
    id: str
    name: str


class Entity2TestValidationException(ValidationException):
    def __init__(self, e: Exception):
        super().__init__(e, "Entity2Test validation error", "ERR999")


@entity(id_field="user_id", validation_exception=Entity2TestValidationException)
class Entity2Test(BaseModel):
    user_id: str
    name: str


def test_Entity_Pydanticの初期化方法で初期化しIDで比較可能():
    john = Entity1Test(id="id1", name="John")
    alice = Entity1Test(id="id2", name="Alice")

    assert john.id == "id1"
    assert john.name == "John"

    assert alice.id == "id2"
    assert alice.name == "Alice"

    assert john != alice

    john2 = Entity1Test.new("id1", name="John2")

    assert john == john2


def test_Entity_自動生成されるnew関数を利用して初期化しIDで比較可能():
    john = Entity1Test.new("id1", name="John")
    alice = Entity1Test.new("id2", "Alice")

    assert john.id == "id1"
    assert john.name == "John"

    assert alice.id == "id2"
    assert alice.name == "Alice"

    assert john != alice

    john2 = Entity1Test.new("id1", name="John2")

    assert john == john2


def test_Entity_id_fieldを指定して初期化しIDで比較可能():
    john = Entity2Test.new("id1", name="John")
    alice = Entity2Test.new("id2", "Alice")

    assert john.user_id == "id1"
    assert john.name == "John"

    assert alice.user_id == "id2"
    assert alice.name == "Alice"

    assert john != alice

    john2 = Entity2Test.new("id1", name="John2")

    assert john == john2


def test_Entity_異なるEntityは同じIDでも異なるものとして扱われる():
    john = Entity1Test.new("id1", name="John")
    alice = Entity2Test.new("id1", "Alice")

    assert john != alice


def test_Entity_BaseModelを継承していない場合はエラー():
    class NotBaseModel():
        pass

    try:
        entity()(NotBaseModel)
        assert False
    except ValueError as e:
        assert str(e) == "Entity class must inherit BaseModel"


def test_Entity_初期化時の引数が足りない場合はエラー():
    try:
        Entity1Test.new()
        assert False
    except ValidationException as e:
        assert str(
            e) == "[NOT DEFINED ERROR CODE] Entity1Test validation error"

    try:
        Entity1Test.new("id1")
        assert False
    except ValidationException as e:
        assert str(
            e) == "[NOT DEFINED ERROR CODE] Entity1Test validation error"


def test_Entity_例外クラスを指定しているEntityは指定の例外が発生する():
    try:
        Entity2Test.new()
        assert False
    except Entity2TestValidationException as e:
        assert str(e) == "[ERR999] Entity2Test validation error"
    except Exception as e:
        assert False


@entity()
class Entity3Test(BaseModel):
    id: str
    name: str
    temp: str

    @classmethod
    def new(cls, id, name):
        return cls(id=id, name=name, temp="temp")


def test_entity_newメソッドが定義されている場合はそのメソッドを利用して初期化():
    john = Entity3Test.new("id1", "John")
    assert john.id == "id1"
    assert john.name == "John"
    assert john.temp == "temp"
