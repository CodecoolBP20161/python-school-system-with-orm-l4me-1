from models import *
import unicodedata
import string


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()

    @property
    def full_name(self):
        return self.first_name+" "+self.last_name

    @property
    def email(self):
        formatted_name = ''.join(x for x in unicodedata.normalize('NFKD', self.full_name) if x in string.ascii_letters)
        return 'l4mecc+{}@gmail.com'.format(formatted_name).lower()
