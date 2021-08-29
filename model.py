from pydantic import BaseModel
class CalculateRequest(BaseModel):
    A: int
    B: int
    class Config:
        title = "Запрос на сложение A и B"
        fields = dict(
            A=dict(
                title="Первое слагаемое"
            ),
            B=dict(
                title="Второй слагаемое"
            )
        )
class CalculateResponse(BaseModel):
    token: int

    class Config:
        title = "Ответ на запрос сложения A и B"
         
        fields = dict(
           
            token=dict(
               
                title="Токен для получения результата операции сложения"
                
            )
        )
class ResultResponse(BaseModel):
    token: int
    status:str
    reuslt:int
    class Config:
        title = "Ответ на запрос получения результата сложения A и B"
        fields = dict(
            token=dict(
                title="Токен результата операции сложения"

            ),
            status=dict(
                title="Статус операции сложения"
            ),
             reuslt=dict(
                title="Результат операции сложения"
            )
        )