from src.fastddd.resources import IBaseRepository
from datetime import datetime


def test_継承したクラスでIBaseRepositoryのメソッドを呼び出す():
    class TestIBaseRepository(IBaseRepository[str]):
        def begin(self):
            return "session"

        def nextval(self, model, session):
            return 1

        def commit(self, session):
            print(session)

        def rollback(self, session):
            print(session)

        def close(self, session):
            print(session)

        def now(self):
            return datetime.now()

    repo = TestIBaseRepository()

    session = repo.begin()

    assert session == "session"
    assert repo.nextval("model", session) == 1
