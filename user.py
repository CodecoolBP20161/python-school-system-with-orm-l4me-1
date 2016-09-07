from models import *


class User(BaseModel):
    user_name = CharField(unique=True, null=False)
    password = CharField(null=False)
    access_right = IntegerField(null=False)

    @property
    def get_access(self):
        return {0: "admin", 1: "mentor", 2: "applicant"}[self.access_right]
