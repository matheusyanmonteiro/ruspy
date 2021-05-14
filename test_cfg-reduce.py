"""
# cfg-reduce

Utilizar transformers para obter resultados a partir da árvore sintática.

* Construir um transformer para obter diretamente resultados da interpretação do código.
* Implementar linguagem simples no escopo de uma calculadora avançada ou algo do gênero.

Em boa medida, os testes desta competência já seguem como consequência de 
implementar as outras corretamente. 

O 
"""
import pytest
from contextlib import redirect_stderr, redirect_stdout
import io 

@pytest.mark.parametrize(
    "name,val", {"simple": 3, "math": 5.0, "math2": True, "math3": "seq 1 2 3 4"}.items()
)
def test_exemplos(name, val, mod):
    with open(mod.PATH / "exemplos" / f"{name}.rpy") as fd:
        src = fd.read()
    print(f"Testando código fonte:\n{src}")

    fd = io.StringIO()
    stdout = None
    with redirect_stdout(fd):
        print(mod.pretty(mod.parse_seq(src)))
        stdout = fd.getvalue()
    assert mod.eval(src) == val or stdout
