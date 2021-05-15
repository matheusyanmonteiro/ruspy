"""
# re-basico 

Criar padrões de regex simples a partir de operações básicas. 

Este exercício verifica apenas padrões que formam números inteiros simples em 
Ruspy.

Modifique a regra de símbolo terminal INT para para aceitar todos os inteiros
abaixo:

    42, 0_0, 000, 01, 1_000_000, 0__0__0, 123456789

Também é necessário modificar o método INT do transformer para realizar a 
conversão de inteiros para o Python.
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
    if is_exec:
        grammar = grammar_mod
    else:
        grammar = grammar_expr
    try:

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

#
# Testes
#
@pytest.mark.parametrize(
    "ex", "42, 0_0, 000, 01, 1_000_000, 0__0__0, 123456789".split(", ")
)
def test_valid_examples(ex, mod):
    check_valid_token(ex, mod, int)


@pytest.mark.parametrize("ex", "_1, __1, 12A".split(", "))
def test_invalid_examples(ex, mod):
    with pytest.raises((AssertionError, lark.LarkError)):
        print("Resultado de token inválido: ", check_valid_token(ex, mod, int))


def test_random_examples(mod):
    for _ in range(150):
        check_valid_token(rint(), mod)


def check_valid_token(ex, mod, typ=None):
    print(f"Testando: {ex} ({typ or '...'})")
    seq = mod.lex_list(ex)
    try:
        [tk] = seq
    except ValueError:
        raise AssertionError(f"erro: esperava token único, obteve sequência {seq}")

    if typ is not None:
        val = mod.transform(tk)
        assert isinstance(
            val, typ
        ), f"tipo errado {tk} ({tk.type}): esperava {typ}, obteve {type(val)}"

    return seq


#
# Funções auxiliares
#
digits = "123456789"
prob = lambda p: random() < p
randrange = lambda a, b: range(a, randint(a, b) + 1)
digit = lambda: choice(digits)
rint = lambda: digit() + "".join(
    "_" if prob(0.25) else digit() for _ in randrange(0, 10)
)


def check_int(ex: str):
    n = ex.replace("_", "")
    assert not ex.startswith("_")
    assert n
    assert n.isdigit()
