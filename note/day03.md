## python
```
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
}
```
This is a dictionary case, with symbol `{}`

`raise` keyword will throw a error actively.

```
def cal(expr: str) -> dict
```
Defining a function like this, `cal` is a function name, `str` represents string type, `-> dict` is return value type.

## content
1. define the tools: calculator, get_weather.
2. let the model decide to use which tool.
3. execute the tools program in local PC.
4. return the result with a new message type: `role=tool`.
