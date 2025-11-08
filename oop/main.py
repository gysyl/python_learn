class Counter:
    def __init__(self, start: int = 0):
        self.value = start

    def increment(self, step: int = 1) -> int:
        self.value += step
        return self.value

    def reset(self) -> None:
        self.value = 0

class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        
    def __str__(self) -> str:
        return f"Student(name={self.name}, age={self.age})"
    
    def study(self, subject: str) -> None:
        print(f"{self.name} is studying {subject}")

    def play(self, game: str) -> None:
        print(f"{self.name} is playing {game}")

if __name__ == "__main__":
    c = Counter()
    print(c.increment())
    print(c.increment(2))
    c.reset()
    print(c.value)
    
    s = Student("Alice", 18)
    print(s)
    s.study("Math")
    s.play("chess")
