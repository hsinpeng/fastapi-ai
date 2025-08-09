import sys
from datetime import date
from pydantic import BaseModel, field_validator

##### Test Pydantic #####
class User(BaseModel):
    id: int
    name: str
    birthday: date

    def __str__(self):
        return f'User(id={self.id}, name={self.name}, birthday={self.birthday})'
    
    @field_validator('id')
    def id_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('id must be positive')
        return v

    @field_validator('name')
    def name_must_be_capitalized(cls, v):
        if v[0].islower():
            raise ValueError('name must be capitalized')
        return v

    @field_validator('birthday')
    def birthday_must_be_after_2000(cls, v):
        if v.year < 2000:
            raise ValueError('birthday must be after 2000')
        return v 

##### Test Dunder Functions #####
class Counter:
    value:int
    def __init__(self, value):
        self.value = value
    
    def count_up(self):
        self.value += 1

    def count_down(self):
        self.value -= 1

    def __str__(self):
        return f"{self.value}"
    
    def __add__(self, other):
        if isinstance(other, Counter):
            return self.value + other.value
        raise Exception("Invalid type!")



###############################################
def main():
    try:
        print("Main Test Program")

        opt = 0
        match opt:
            case 0:
                print("----- Pydantic Test 1 -----")
                print(User(id=0, name='John', birthday=date(2000, 1, 1)))
                print("OK")

                print("----- Pydantic Test 2 -----")
                print(User(id=-1, name='John', birthday=date(2000, 1, 1)))
                print("OK")

                print("----- Pydantic Test 3 -----")
                print(User(id='str', name='John', birthday=date(2000, 1, 1)))
                print("OK")

            case 1:
                print("----- Dunder Test -----")
                count1 = Counter(1)
                count2 = Counter(1)

                count1.count_up()
                count2.count_up()

                print(count1, count2)
                print(count1 + count2)
                print(count1 + 3)
            
            case _:
                print(f"Error: Wrong opt({opt})!")

    except ValueError as ve:
        return str(ve)

if __name__ == "__main__":
    sys.exit(main())