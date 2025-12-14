from typing import Annotated, Optional, List
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
SurnameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
start_DateStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
end_DateStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]

AgeInt = Annotated[int, Ge(0), Le(150)]

class BookingCreate(BaseModel):
    first_name: NameStr
    surname: SurnameStr
    start_Date: start_DateStr
    end_Date: end_DateStr

class BookingRead(BaseModel):
    booking_id: int
    first_name: NameStr
    surname: SurnameStr
    start_Date: start_DateStr
    end_Date: end_DateStr

    model_config = ConfigDict(from_attributes=True)

class BookingUpdate(BaseModel):
    first_name: Optional[NameStr] = None
    surname: Optional[SurnameStr] = None
    start_Date: Optional[start_DateStr] = None
    end_Date: Optional[end_Date] = None