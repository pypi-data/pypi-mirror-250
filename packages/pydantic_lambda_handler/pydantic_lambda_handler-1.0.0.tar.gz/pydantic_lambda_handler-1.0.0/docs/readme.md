# Pydantic Lambda handler

The aim is to create something between FastApi and Chalice.
So same familiar interface as FastAPI, where it makes sense, for aws lambda.

The outputs an open api spec as well as a cdk conf which can be used to generate aws gateway and lambdas.

The open api spec is generated and validated using openapi-spec-validator, but this is still in an alpha phase so please let me know if you have any problems.

## Basic usage

handler_app.py
```
from pydantic_lambda_handler.main import PydanticLambdaHandler

app = PydanticLambdaHandler(title="PydanticLambdaHandler")
```
{: .language-python}

Then in a file ending with `_handler.py` or `_handlers.py`, or in the folder `handlers` add ...

```
app.get("/")
def your_handler():
    return {"success": True}
```
{: .language-python}

## url parameters
url parameters will always be evaluated first, then query parameters.
For that reason you cannot have a query parameter that matches the path parameter unless you use an alias
```
@app.get("/items/{item_id}")
def handler_with_type_hint(item_id: int):
    return {"item_id": item_id}
```
{: .language-python}

## query parameters

query parameters can be single or multivalue

```
@app.get("/query_multivalue_param")
def query_multi_param(sausages: Optional[list[int]]):
    return {"sausages": sausages}
```
{: .language-python}

## headers parameters

Headers can be added using the Header param

```
@app.get("/with_headers")
def with_headers(host: Union[str, None] = Header(default=None, alias="Host")):
    return {"host": host}
```
{: .language-python}


## context object

You can access the lambda context using
```
from awslambdaric.lambda_context import LambdaContext

@app.get("/context")
def with_context(lambda_context: LambdaContext):
    return {"context": lambda_context.get_remaining_time_in_millis()}
```
{: .language-python}


## response model

If response model needs to be a list, do need to adjust the model like so

https://docs.pydantic.dev/latest/concepts/models/#rootmodel-and-custom-root-types
```
class ListFunModel(RootModel):
    root: list[FunModel]
```
{: .language-python}

## Error handling

```
@app.get("/error", errors=[(418, ValueError)])
def error():
    raise ValueError("nope")

# {
#    "statusCode": 418,
#    "body": {"detail": [{"msg": "nope", "type": "ValueError"}]}
# }
```
{: .language-python}

## Base Url

To get the base url of your lambda function

```commandline
@app.get("/base_url")
def error():
    app.base_url
```

The base url will include the stage name

# Hooks

There is a hook class `BaseHook` which allows you to extend the functionality of
the api.