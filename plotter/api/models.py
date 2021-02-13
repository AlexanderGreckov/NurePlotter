import pydantic


class Point(pydantic.BaseModel):
    x_value: int
    y_value: int
