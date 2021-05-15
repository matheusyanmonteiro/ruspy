"""
# re-prog

Converter e associar expressões regulares da teoria de compiladores com expressões regulares escritas em linguagem de programação. 

* Criar e manipular expressões regulares em Python ou outra linguagem de programação.
* Escrever expressões do livro texto na sintaxe utilizada em linguagens de programação.

---- 

Esta é uma competência virtual, já que quem resolver lex-re já ganha automaticamente
re-prog. Caso você tenha conseguido traduzir as expressões regulares de cada 
categoria individualmente, mas não conseguiu fazer com que elas funcionem corretamente
em conjunto no lexer, pode submeter as expressões na variável

    RE_PROG = {
        "DEC": r"...",
        "HEX": r"...",
        "OCT": r"...",
        "BIN": r"...",
        "FLOAT": r"...",
        "ID": r"...",
    }

Lembrando mais uma vez: se os testes de lex-re passaram, NÂO PRECISA submeter
esta resposta já que a pontuação é conferida automaticamente.
"""
import pytest


def test_verificações_básicas():
    pytest.skip("o código de teste ainda não está pronto")