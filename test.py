r"""

**TODO:** `exec_` is not the right name here, it does not behave like `exec`.
Find a better name.

Execute some remote code, get stdout

    >>> exec_("print(1 + 1)")
    '2\n'

Get stdout, cleaned-up remotely    

    >>> exec_("print(1 + 1, end='', flush=True)")
    '2'

The kernel you are interacting with is persistent:    

    >>> exec_("a = 1")
    ''

    >>> exec_("a += 1")
    ''

    >>> exec_("print(a)")
    '2\n'

Expressions "print" nothing to stdout by default:

    >>> exec_("1 + 1")
    ''

but it's pretty easy to solve that with a helper if this is what you need:

    >>> def eval_(expr):
    ...     cmd = f"_ = {expr}; print(_, end='', flush=True)"
    ...     return exec_(cmd)

    >>> eval_("1 + 1")
    '2'

    >>> eval_("'Hello' + ' ' + 'world!'")
    'Hello world!'

Customize `eval_` if you need to; the following variant could make sense:    

    >>> def eval_repr(expr):
    ...     cmd = f"_ = {expr}; print(repr(_), end='', flush=True)"
    ...     return exec_(cmd)
    ...

    >>> eval_repr("1 + 1")
    '2'

    >>> eval_repr("'Hello' + ' ' + 'world!'")
    "'Hello world!'"

Behavior in the presence of remote errors? Unspecified? Which means that you
have to wrap your code command into some error-managing stuff? Sure, why not.
The only question maybe is are we robust in face of errors: do we keep
spinning whatever happens? I'd say yes and that is our only guarantee.

    >>> _ = exec_("raise RuntimeError()")

    >>> _ = exec_("1 + ")

    >>> _ = exec_("jsdkljqslkdsj")

    >>> error_handler = '''
    ... def try_(code):
    ...    try:
    ...       exec(code, globals())
    ...    except Exception as error:
    ...       output = f"{type(error).__name__}: {error}"
    ...       print(output)
    ... '''
    >>> exec_(error_handler)
    ''
    >>> def exec_try(code):
    ...    return exec_(f"try_({code!r})")
    ...


    >>> exec_try("print(1 + 1)")
    '2\n'
    
    >>> exec_try("1 + ") # doctest: +ELLIPSIS
    'SyntaxError: invalid syntax ...\n'

    >>> exec_try("a = pi + e")
    "NameError: name 'pi' is not defined\n"

    >>> json_result_handler = '''
    ... import json
    ... import io
    ... def json_(code):
    ...    try:
    ...        output_stream = io.StringIO()
    ...        with redirect_stdout(output_stream):
    ...            ast.parse(code, mode="exec")
    ...            exec(code, globals())
    ...        output = output_stream.getvalue()
    ...        json_output = {"error": None, "output": output}
    ...    except Exception as e:
    ...        error = f"{type(e).__name__}: {e}"
    ...        json_output = {"error": error, "output": None}
    ...    print(json.dumps(json_output), end="", flush=True)
    ... '''
    >>> exec_(json_result_handler)
    ''
    >>> def exec_json(code):
    ...    return exec_(f"json_({code!r})")
    ...
    
    >>> exec_json("print(1 + 1)")
    '{"error": null, "output": "2\\n"}'

    >>> exec_json("a = 3")
    '{"error": null, "output": ""}'

    >>> exec_json("print(a, end='', flush=True)")
    '{"error": null, "output": "3"}'

    >>> exec_json("abracadabra")
    '{"error": "NameError: name \'abracadabra\' is not defined", "output": null}'

    >>> exec_json("raise RuntimeError('Oops, I did it again!')")
    '{"error": "RuntimeError: Oops, I did it again!", "output": null}'


"""


# Python Standard Library
from multiprocessing import Process
import time

# Third-Party Libraries
import requests

# Local
import toupie

def exec_(input: str) -> str:
    response = requests.post(
        url="http://127.0.0.1:8000", 
        headers={"Content-Type": "text/plain"}, 
        data=input
    )
    response.raise_for_status()
    return response.text

def spin_background(wait: float = 1.0) -> Process:
    p = Process(target=lambda: toupie.spin(verbose=-1), daemon=True)
    p.start()
    time.sleep(wait)
    return p

spin_background()