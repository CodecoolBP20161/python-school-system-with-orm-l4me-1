from models import *


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()

    @property
    def full_name(self):
        return self.first_name+" "+self.last_name
