from pydantic import BaseModel, EmailStr, constr, conint

class User(BaseModel):
    user_id: int
    first_name: constr(min_length=2, max_length=50)
    surname: constr(min_length=2, max_length=50)
    age: conint(gt=18)
    email: EmailStr
    phoneNo: constr(min_length=10, max_length=12)
    booking_number: constr(min_length=2, max_length=50)

class Booking_Info(BaseModel):
    booking_id: int
    first_name: constr(min_length=2, max_length=50)
    surname: constr(min_length=2, max_length=50)
    start_Date: constr(min_length=10, max_length=10)
    end_Date: constr(min_length=10, max_length=10)
