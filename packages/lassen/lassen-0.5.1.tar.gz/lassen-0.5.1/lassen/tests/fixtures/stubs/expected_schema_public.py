from pydantic import BaseModel, Field, ConfigDict
from MOCKED_PACKAGE import Union
from MOCKED_PACKAGE import str

from datetime import datetime
from enum import Enum



# Shared properties
class UserStubBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )


# STORE: SEARCH FILTER PROPERTIES
class UserStubFilter(UserStubBase):

    pass



# API/STORE: CREATE PROPERTIES
class UserStubCreate(UserStubBase):

    password: str



# API/STORE: UPDATE PROPERTIES
class UserStubUpdate(UserStubBase):

    pass



# API/STORE: RETRIEVE PROPERTIES
class UserStub(UserStubBase):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(description='First name of the user', examples=['John'])

    last_name: Union[str, None] = Field(description='Last name of the user', examples=['Smith'])

    password: str
