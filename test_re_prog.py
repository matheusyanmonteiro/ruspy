"""
# re-prog

Converter e associar expressões regulares da teoria de compiladores com 
expressões regulares escritas em linguagem de programação
Criar e manipular expressões regulares em Python ou outra linguagem de programação.

Vamos testar esta habilidade traduzindo as regras para símbolos terminais de 
Rust em expressões regulares de Python. Esta habilidade verifica os tipos 
numéricos em 

* Inteiros: https://doc.rust-lang.org/reference/tokens.html#integer-literals
* Floats: https://doc.rust-lang.org/reference/tokens.html#floating-point-literals
* Comentários no formato C, tanto no estilo // até o fim da linha
  quanto no estilo /* bloco */. O Rust possui regras mais sofisticadas, mas vamos
  ignorá-las na atividade.
* Identificadores: https://doc.rust-lang.org/reference/identifiers.html
  (mas a última é trivial, porque a referência já fornece a expressão regular).

Quem optar por implementar as regras de string e raw string ganha também a 
habilidade opcional re-adv*, mas isto é testado pelo arquivo re_adv_V1. Se não 
estiver interessado(a) nesta competência, implemente strings como sequências de
letras e espaços entre aspas. 
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
