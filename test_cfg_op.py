"""
# cfg-op

Representar precedência de operadores em gramática (E)BNF

* Reconhecer relação entre gramática e precedência.
* Definir gramática para obter uma precedência desejada.
* Implementar corretamente exemplos clássicos como uma calculadora.

As regras de precedência da gramática do ruspy estão incorretas. Implemente a
precedência e associatividade de operadores de acordo com as regras em 

https://doc.rust-lang.org/reference/expressions.html?highlight=operator%20precedence#expression-precedence

Note que alguns operadores foram omitidos no ruspy (como *, & e &mut unários).
Minha sugestão é se guiar pelos testes para verificar o que falta ser implementado
e o que está correto na gramática.
"""
import pytest
import lark

import pytest
from pytest import approx as _approx
from hypothesis import given
from hypothesis import strategies as st

PYSOURCE = "operadores.py"


def approx(x, rel=1e-6, abs=1e-6, nan_ok=False):
    return _approx(x, rel=rel, abs=abs, nan_ok=nan_ok)


def ms():
    return st.integers(min_value=-100, max_value=100)


def ns():
    return st.integers(min_value=1, max_value=100)


def xs():
    return (
        st.floats(min_value=0.1, max_value=1000)
        | st.floats(min_value=-1000, max_value=-0.1)
        | st.just(0.0)
    )


def ys():
    return st.floats(min_value=0.1, max_value=1000)


class TestOperators:
    @pytest.fixture(scope="session")
    def eval(self, mod):
        def eval(src):
            print(f'eval> {src}')
            res = mod.expr(src)
            print(mod.grammar_expr.parse(src).pretty())
            print('=>', res, '\n\n')
            return res
        return eval

    @given(xs(), ys(), ms())
    def test_soma_subtração(self, eval, x, y, n):
        assert eval(f"{x} + {y}") == approx(x + y)
        assert eval(f"{x} + {y} + {n}") == approx((x + y) + n)

        assert eval(f"{x} - {y}") == approx(x - y)
        assert eval(f"{x} - {y} - {n}") == approx((x - y) - n)

        assert eval(f"{x} + {y} - {n}") == approx((x + y) - n)
        assert eval(f"{x} - {y} + {n}") == approx((x - y) + n)

    @given(xs(), ys(), ns())
    def test_multiplicação(self, eval, x, y, n):
        assert eval(f"{x} * {y}") == approx(x * y)
        assert eval(f"{x} * {y} * {n}") == approx((x * y) * n)

        assert eval(f"{x} / {y} * {n}") == approx((x / y) * n)
        assert eval(f"{x} * {y} / {n}") == approx((x * y) / n)

        assert eval(f"{x} + {y} * {n}") == approx(x + (y * n))
        assert eval(f"{x} * {y} + {n}") == approx((x * y) + n)

    @given(ms() | xs(), ns() | ys())
    def test_divisao_funciona_de_forma_especial_para_inteiros(self, eval, a, b):
        print(f"ops: {a}, {b}")
        if isinstance(a, int) and isinstance(b, int):
            assert eval(f"{a} % {b}") == a % b

            print("ERRO: divisão de 2 inteiros deve dar inteiro, modifique o transformer")
            assert eval(f"{a} / {b}") == a // b
        else:
            print("ERRO: divisão com algum float retorna float")
            assert eval(f"{a} / {b}") == approx(a / b)

    @given(ms(), ns())
    def test_operação_de_bitshift(self, eval, m, n):
        assert eval(f"{m} >> {n}") == m >> n
        assert eval(f"{m} << {n}") == m << n

    @given(ms(), ns(), ns())
    def test_precedência_de_operação_de_bitshift(self, eval, m, n, b):
        assert eval(f"{m} << {n} + {b}") == m << (n + b)
        assert eval(f"{m} + {b} << {n}") == (m + b) << n

    @given(ms(), ns())
    def test_operações_bitwise(self, eval, m, n):
        assert eval(f"{m} & {n}") == m & n
        assert eval(f"{m} ^ {n}") == m ^ n
        assert eval(f"{m} | {n}") == m | n

    @given(ms(), ns(), ns())
    def test_associatividade_de_operação_bitwise(self, eval, m, n, b):
        assert eval(f"{m} & {n} & {b}") == (m & n) & b
        assert eval(f"{m} ^ {n} ^ {b}") == (m ^ n) ^ b
        assert eval(f"{m} | {n} | {b}") == (m | n) | b

    @given(ms(), ns(), ns())
    def test_precedência_de_operação_bitwise(self, eval, m, n, b):
        assert eval(f"{m} & {n} >> {b}") == m & (n >> b)
        assert eval(f"{m} >> {n} & {b}") == (m >> n) & b

        assert eval(f"{m} & {n} << {b}") == m & (n << b)
        assert eval(f"{m} << {n} & {b}") == (m << n) & b

        assert eval(f"{m} & {n} ^ {b}") == (m & n) ^ b
        assert eval(f"{m} ^ {n} & {b}") == m ^ (n & b)

        assert eval(f"{m} ^ {n} | {b}") == (m ^ n) | b
        assert eval(f"{m} | {n} ^ {b}") == m | (n ^ b)

    @given(ms(), ns())
    def test_operações_de_comparação(self, eval, m, n):
        assert eval(f"{m} > {n}") == (m > n)
        assert eval(f"{m} < {n}") == (m < n)
        assert eval(f"{m} >= {n}") == (m >= n)
        assert eval(f"{m} <= {n}") == (m <= n)
        assert eval(f"{m} == {n}") == (m == n)
        assert eval(f"{m} !=  {n}") == (m != n)

    def test_operações_booleanas(self, eval):
        for m in [True, False]:
            for n in [True, False]:
                assert eval(f"{m} && {n}".lower()) == (m and n)
                assert eval(f"{m} || {n}".lower()) == (m or n)

    @given(st.sampled_from([0, 1, 2, 3]))
    def test_precedencia_e_associatividade_de_operações_booleanas(self, eval, b):
        for m in [True, False]:
            for n in [True, False]:
                assert eval(f"{m} && {n} && {b}".lower()) == (m and n and b)
                assert eval(f"{m} || {n} || {b}".lower()) == (m or n or b)
                assert eval(f"{m} && {n} || {b}".lower()) == (m and n or b)
                assert eval(f"{m} || {n} && {b}".lower()) == (m or n and b)

    @given(ns(), ns())
    def test_operador_range(self, eval, m, n):
        n += m
        assert list(eval(f"{m} .. {n}")) == [*range(m, n)]
        assert list(eval(f"{m} ..= {n}")) == [*range(m, n), n]

    @pytest.mark.parametrize(
        "src",
        [
            "a..b..a",
            "a..=b..=a",
            "a..=b..a",
            "a..b..=a",
            "a > b > c",
            "a < b < c",
            "a == b == c",
            "a !== b !== c",
        ],
    )
    def test_códigos_inválidos(self, src, mod):
        with pytest.raises(lark.LarkError):
            print(f"Código inválido foi aceito: {src!r}")
            print(mod.parse(src).pretty())

    @pytest.mark.parametrize(
        "src",
        [
            f"x {op} y"
            for op in ".. ..= || && == != > < >= <= & | ^ << >> + - * / %".split()
        ],
    )
    def test_códigos_válidos(self, src, mod):
        print(f"Testando {src!r}")
        mod.parse(src)
