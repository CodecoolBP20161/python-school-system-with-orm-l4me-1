from models import *


class School(BaseModel):
    location = CharField()

    class Meta:
        order_by = ['location']
