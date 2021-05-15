"""
# lex-ler

Compreender a motivação e mecanismos da análise léxica. 

* Separar um código fonte em tokens e lexemas.
* Identificar os diferentes tipos de lexemas.
* Identificar lexemas em linguagens de programação reais como Python ou C.

----

Atenção! Este não é um exercício de programação, mas sim de compreensão dos 
conceitos relacionados à análise léxica. Ainda assim, a resposta é corrigida
de forma automatizada. 

Considere o código ruspy abaixo:

    // Fatorial
    fn fat(n: int) {
        r = n
        for i in 1..n {
            r *= i
        }
        r
    }

Separe este programa em lexemas e salve-os como uma lista de strings na variável:

    FAT_LEXEMAS = ["fn", "fat", ...] 

Os comentários são removidos da lista de lexemas, já que não interessam à análise
semântica. Você pode gerar esta lista de forma manual, automática ou semi-automática.
A única parte importante é obter o valor correto no final.

Na segunda parte faça a classificação de cada lexema em sua categoria e salve
como 
    
    FAT_TOKENS = ["fn FN", "fat ID", ...] 

ou seja, cada string contêm o lexema e a categoria de não-terminal separados
por um espaço. Considere as seguintes categorias:

    ID  - identificadores 
    INT - inteiros
    OP  - operadores binários
    LBRACE/RBRACE - chaves (abrir/fechar) 
    LPAR/RPAR     - parênteses (abrir/fechar) 

Cada palavra reservada possui sua categoria a parte como FN, IF, etc.
"""
import pytest
import lark


@pytest.mark.parametrize("grp", "ID INT BIN_INT OCT_INT HEX_INT FLOAT".split())
def test_exemplos_positivos(grp, mod, data):
    for ex in sorted(data(grp), key=len):
        typ = None
        if grp.endswith("INT"):
            typ = int
        if grp.endswith("FLOAT"):
            typ = float
        check_valid_token(ex, mod, grp, typ=typ)


def test_comentários(mod, data):
    grp = "COMMENT"
    for ex in sorted(data(grp), key=len):
        print(f"Testando: {ex!r} ({grp})")
        seq = mod.lex_list(ex)
        if seq:
            raise AssertionError(f"erro: esperava comentário, obteve sequência {seq}")


@pytest.mark.parametrize("grp", "ID INT BIN_INT OCT_INT HEX_INT FLOAT COMMENT".split())
def test_exemplos_negativos(grp, mod, data):
    for ex in sorted(data(grp + "_bad"), key=len):
        print(f"Testando: {ex!r} ({grp})")
        try:
            seq = mod.lex_list(ex)
        except lark.LarkError:
            continue

        if grp == "COMMENT" and not seq:
            raise AssertionError(f"aceitou elemento: {ex}")
        elif len(seq) == 1 and seq[0].type == grp and seq[0] == ex:
            raise AssertionError(f"aceitou elemento: {seq}")


def check_valid_token(ex, mod, grp, typ=None):
    print(f"Testando: {ex!r} ({grp})")
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
