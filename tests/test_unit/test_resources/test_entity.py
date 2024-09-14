from src.fastddd.resources import Entity


def test_継承したクラスでEntityのクラスメソッドを呼び出す():
    class TestEntity(Entity):
        user_id: str
        name: str

        @classmethod
        def new(cls, id: str, name: str) -> "TestEntity":
            return cls(user_id=id, name=name).set_id_field("user_id")

    entity1 = TestEntity.new("id2", "John")
    entity2 = TestEntity.new("id2", "Alice")

    assert entity1 == entity2

    assert TestEntity.generate_id() != Entity.generate_id()
    assert TestEntity.generate_secret() != Entity.generate_secret()
    assert TestEntity.now() != Entity.now()
