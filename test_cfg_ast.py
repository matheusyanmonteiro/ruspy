"""
# cfg-ast

 Criar árvore sintática

Em boa medida, os testes desta competência já seguem como consequência de 
implementar as outras corretamente. 

Você deve ser capaz de organizar a gramática do Lark de forma que os exemplos
no módulo exemplos sejam analisados corretamente, produzindo as árvores sintáticas
corretas. Se o seu módulo definir um transformer chamado AstTransform, ele será
utilizado na comparação.

Note que os testes podem simplificar um pouco a árvode sintática com relação ao
que o seu código realmente retorna.
"""

import pytest
import lark
import difflib

mods = {"fib", "pair"}


class Simplify(lark.InlineTransformer):
    def null(self, *args):
        if len(args) == 1:
            return args[0]
        return lark.Tree("null", list(args))

    def name(self, x):
        return x

    def lit(self, x):
        return x


def simplify(ast):
    return Simplify().transform(ast)


@pytest.mark.parametrize("name", ["fib", "pair", "simple", "math", "math2", "math3"])
def test_exemplos(name, mod):
    Transform = getattr(mod, "AstTransform", None)
    if Transform:
        transform = Transform().transform
    else:
        transform = lambda x: x

    with open(mod.PATH / "exemplos" / f"{name}.rpy") as fd:
        src = fd.read()
    print(f"Testando código fonte:\n{src}")

    with open(mod.PATH / "exemplos" / f"{name}.ast") as fd:
        target = fd.read().strip()
        tree = mod.parse_mod(src) if name in mods else mod.parse_seq(src)
        ast = simplify(transform(tree)).pretty().strip()

    if target != ast:
        print("\n\nÁrvores diferentes!")
        if len(target) == 0:
            print("Saída:")
            print(ast)
            print("\nEsperado:")
            print(target)
        else:
            diff = difflib.ndiff(ast.splitlines(), target.splitlines())
            print('Diff:')
            print('\n'.join(diff))
        raise AssertionError("árvores sintáticas diferem!")
