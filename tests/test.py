from dataclasses import dataclass
from typing import Callable, Self


class Test:
    name: str
    func: Callable[[any], bool]
    allTests: list[Self] = []

    def __init__(self, name: str, func: Callable[[any], bool]) -> None:
        self.name = name
        self.func = func

    @classmethod
    def test(cls, func: Callable[[any], bool]) -> Self:
        test = cls(func.__name__, func)
        cls.allTests.append(test)
        return test

    def __call__(self, *args, **kwds):
        try:
            print(f"Test '{self.name}': {'✅ Passed' if self.func(*args, **kwds) else '❌ Failed'}")
        except Exception as e:
            print(f"Test '{self.name}': ⚠️ Raised an exception: {e} ")
    
    @classmethod
    def runAll(cls) -> None:
        for test in cls.allTests:
            test()


def testing():
    @Test.test
    def failingTest() -> bool:
        return False

    @Test.test
    def successfulTest() -> bool:
        return True

    @Test.test
    def exceptionTest() -> bool:
        raise TypeError

    Test.runAll()


if __name__ == "__main__":
    testing()

