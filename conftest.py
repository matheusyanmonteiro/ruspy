"""
Funcionalidades compartilhadas por todos modulos de teste
"""
from types import SimpleNamespace
from random import choice, random, randint
import pytest
import lark
import os
from pathlib import Path

#
# Recursos
#
EXTRA_SRC = r'''
grammar_expr = Lark(GRAMMAR, parser="lalr", start="seq")
grammar_mod = Lark(GRAMMAR, parser="lalr", start="mod")

def eval(src):
    return _eval_or_exec(src, is_exec=False)

def module(src) -> dict:
    return _eval_or_exec(src, is_exec=True)

def run(src):
    mod = module(src)
    main = mod.get("main")
    if not main:
        raise RuntimeError('módulo não define uma função "main()"')
    main()

def _eval_or_exec(src: str, is_exec=False) -> Any:
    try:
        grammar = grammar_mod if is_exec else grammar_expr
        tree = grammar.parse(src)
    except LarkError:
        print("Erro avaliando a expressão: \n{src}")
        print("\nImprimindo tokens")
        for i, tk in enumerate(grammar.lex(src), start=1):
            print(f" - {i}) {tk} ({tk.type})")
        raise
    transformer = RuspyTransformer()
    result = transformer.transform(tree)

    if isinstance(result, Tree):
        print(tree.pretty())
        raise NotImplementedError(
            f"""
não implementou regra para lidar com: {tree.data!r}.
Crie um método como abaixo na classe do transformer.
    def {tree.data}(self, ...): 
        return ... 
"""
        )
    return result
'''


@pytest.fixture(scope="module")
def mod():
    mod = os.environ.get("RUSPY", "")
    if mod:
        mod = "-" + mod
    path = Path.cwd() / ("ruspy" + mod + ".py")
    with open(path) as fd:
        src = fd.read()
    ns = {}
    exec(src, ns)

    if "GRAMMAR" not in ns:
        raise ValueError("não é permitido modificar o nome da variável GRAMMAR")
    if not isinstance(ns["GRAMMAR"], str):
        raise ValueError("a gramática deve ser uma string")
    if "RuspyTransformer" not in ns:
        raise ValueError("Não encontrou o RuspyTransformer")

    exec(EXTRA_SRC, ns)
    ns["lex"] = lex = ns["grammar_expr"].lex
    ns["parse"] = ns["grammar_expr"].parse
    ns["parse_mod"] = ns["grammar_mod"].parse
    ns["lex_list"] = lambda s: list(lex(s))
    ns["transformer"] = transformer = ns["RuspyTransformer"]
    ns["transform"] = lambda ast: [*transformer()._transform_children([ast])][0]
    lark.InlineTransformer
    return SimpleNamespace(**ns)


@pytest.fixture(scope="session")
def aux():

    return SimpleNamespace(
        check_int=check_int,
        prob=prob,
        digit=digit,
        randrange=randrange,
        rint=rint,
    )


prob = lambda p: random() < p
digit = lambda ds="123456789": choice(ds)
randrange = lambda a, b: range(a, randint(a, b) + 1)
rint = lambda: (
    digit() + "".join("_" if prob(0.25) else digit() for _ in randrange(0, 10))
)


def check_int(ex: str):
    n = ex.replace("_", "")
    assert not ex.startswith("_")
    assert n
    assert n.isdigit()
