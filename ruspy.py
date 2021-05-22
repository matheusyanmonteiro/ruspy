import builtins
import math
import sys
from typing import Any
from lark import Lark, InlineTransformer, LarkError, Token, Tree

# Constantes (algumas tarefas pedem para incluir variáveis específicas nesta
# parte do arquivo)
NAME = "Matheus Yan MOnteiro"
MATRICULA = "18/0127969"
...
FAT_LEXEMAS = ["fn", "fat", "(", "n", ":", "int", ")", 
                "{", "r", "=", "n", "for","i", "in", "1", 
                "..", "n", "{", "r", "*=", "i", "}", "r", "}"]

FAT_TOKENS = ["fn FN", "fat ID", "( LPAR", "n ID", ": OP", "int ID", 
              ") RPAR", "{ LBRACE", "r ID", "= OP", "n ID", "for FOR",
              "i ID", "in IN", "1 INT", ".. OP", "n ID", "{ LBRACE", 
              "r ID", "*= OP", "i ID", "} RBRACE", "r ID", "} RBRACE"]
SUBS_COMENTARIOS_STRINGS = (r"^(\s*)#\s*(.*)", r'\1"""\2"""')
SUBS_REMOVER_COMENTARIOS = (r"#.*", "")

COMP_ORG = """
  Análise Léxica: lê todo o código-fonte, analisando caracter por caracter, separando
  e identificando os tokens que compõem esse código fonte.

  Análise Sintática: Determina se uma cadeia de tokens pode ser gerada por uma gramática.

  Análise Semântica: Usando o resultado da análise léxica e sintática, a análise semântica
  provê métodos que permitem que as estruturas contruídas pela análise sintática sejam 
  avaliadas e executadas.

  Otimização: Analisa o código intermediário que é produzido após a análise semântica e utiliza
  estratégias para produzir um código que execute com bastante eficiência. Essas técnicas detectam
  padrões do código intermediário e substitui por código mais eficiente.

  Emissão de Código: É o momento em que é gerado o código final. Essa etapa pode levar em
  consideração a máquina para o qual o código será gerado e utilizado.
"""

COMP_VS_INTERP_Q1 = """
  Compiladores: Um compilador é um programa de computador que, a partir de um código fonte escrito em uma linguagem compilada, cria um programa semanticamente equivalente, porém escrito em outra linguagem, código objeto. Classicamente, um compilador traduz um programa de uma linguagem textual 

  Interpretadores:  são programas de computador que leem um código fonte de uma linguagem de programação interpretada e o converte em código executável.
"""

COMP_VS_INTERP_Q2 = """
  Compilador de Python: https://www.onlinegdb.com/online_python_compiler
  Interpretador de C: https://gitlab.com/zsaleeba/picoc
"""


REGEX_CROSSWORDS = {
    "intermediate/puzzles/1": "ATOWEL",
    "intermediate/puzzles/2": "WALKER",
    "intermediate/puzzles/3": "FORTY-TWO",
}


# Gramática do Ruspy. (não modifique o nome desta variável, testes dependem disto!)
GRAMMAR = r"""
// Um módulo ruspy é uma sequência de declarações de funções.
// O ruspy executa o módulo chamando a função main() sem nenhum argumento, caso
// ela esteja definida.
// Ex:
//  fn fat(n: int) { if n == 0 { 1 } else { n * fat(n - 1) }}
//
//  fn main() {
//      println("fat(5) =", fat(5))
//  }
mod    : fn+

// Declaração de funções
// Ex:
//     fn fat(n: int) {
//         let tot = n;
//         for i in 1..n {
//             tot = tot * i;
//         }
//         return tot
//     }
//
// O ruspy usa a palavra reservada "fn" de forma similar ao "def" do Python.
// A declaração dos argumentos é semelhante e o corpo da função é delimitado por
// chaves ao invés de utilizar indentação.
fn     : "fn" ID "(" args ")" block 
args   : arg+
arg    : ID ":" ID

// Comandos básicos de ruspy. Verifique a declaração de expr_s e expr_b para 
// saber mais.
?cmd   : expr_s ";"       -> cmd
       | expr_b
       | "let" assign ";" -> let

// A sequência de comandos é a porta de entrada do ruspy no modo "eval". Executamos
// cada comando e o valor resultante corresponde ao valor do último elemento da 
// sequência. 
?seq   : cmd+

// Comandos e controle de fluxo (if, for, while)
// Diferentemente do Python, estes comandos podem ser utilizados como valores
// e salvos em variáveis, argumentos de funções, etc.
// Os comandos for e while sempre retornam null como valor final, enquanto o if 
// retorna o último valor do bloco utilizado.
if_    : "if" expr block "else" block
for_   : "for" ID "in" expr block
while_ : "while" expr block

// Bloco de comandos.
// Ex:
//     {x = 1; y = 2; x + y}
//
// Diferentemente do Python, blocos podem ser utilizados em
// qualquer lugar que aceita um valor como em argumentos de funções
// ou valores de variáveis. O valor do bloco corresponde ao do último
// termo. Caso o último termo contenha um ";" como em {x; y;}, o bloco
// retorna o valor nulo e executa os comandos apenas pelos seus efeitos 
// externos como alteração do valor de variáveis, prints, etc. 
block  : "{" seq "}"

// Atribui um valor a um nome
// Ex:
//    x = 42
//
// Uma atribução também pode ser usada como um valor. Neste caso, dizemos que
// o valor da atribuição corresponde ao valor do lado direito.
// Assim, é possível fazer f(x=1, y=2) para ao mesmo tempo salvar os
// valores 1 e 2 nas variáveis x e y como passar estes mesmos valores para a 
// função f.
assign : ID "=" expr

// Valores básicos do Ruspy. Todas alternativas para expr podem ser utilizadas
// como valores. As expressões são divididas em expr_s e expr_b
?expr  : expr_s 
       | expr_b

// Expressões simples. Exigem ";" numa sequência.
?expr_s: assign
       | lambd

// Expressões com blocos. O ";" é opcional nas sequências.
// Note que ruspy aceita construções curiosas como 
// 
//     x = { y = 1; z = 2; y + z }
//     a = if x > 2 {
//         z = x * 2;
//         z * z
//     } else {
//         println("x pequeno!");
//         x
//     }
?expr_b: block 
       | if_
       | for_
       | while_


// Funções anônimas.
// Ex:
//     |x, y| x + y => lambda x, y: x + y
//
// Lembrando que "lambda x, y: x + y" em python cria uma função equivalente a 
//
//     def f(x, y):
//         return x + y
//
// mas utiliza menos linhas de código. Ruspy é mais flexível porque a expressão
// pode corresponder a um bloco e portanto conter várias linhas de código.
?lambd : "|" args "|" expr
       | range

// Intervalos, incluindo ou não o último elemento
// Ex: 
//  1..5  => 1, 2, 3, 4
//  1..=5 => 1, 2, 3, 4, 5
// Equivale à função range(a, b) do Python. No segundo caso (intervalo inclusivo)
// utilizamos range(a, b + 1), para incluir o valor b em "a ..= b"
?range : and_e ".." and_e
       | and_e "..=" and_e -> irange
       | and_e

// Conectivos lógicos "and" (&&) e "or" (||)
?and_e : and_e "&&" or_e
       | or_e

?or_e  : or_e "||" cmp
       | cmp

// Operadores de comperação
?cmp   : cmp "==" bit      -> eq
       | cmp "!=" bit      -> ne
       | cmp "<"  bit      -> lt
       | cmp ">"  bit      -> gt
       | cmp "<=" bit      -> le
       | cmp ">=" bit      -> ge
       | bit

// Operações bit a bit
?bit   : bit "|" shift     -> or_
       | bit "^" shift     -> xor
       | bit "&" shift     -> and_  
       | shift    

?shift : shift ">>" sum    -> rshift     
       | shift "<<" sum    -> lshift
       | sum

// Operações aritiméticas
?sum   : sum "+" mul       -> add     
       | sum "-" mul       -> sub
       | mul

?mul   : mul "*" typed     -> mul     
       | mul "/" typed     -> div     
       | typed

// Conversão de tipos
// Ex:
//    42 as float => float(42)
//
// Converte valor no lado esquerdo para tipo do lado direito
?typed : typed "as" unary  -> typed     
       | unary

// Operações unárias
// Ex:
//    -x => -x, negativo do número
//    !x => not x, negação lógica
//    x? => verifica se objeto não é nulo. Não será implementado
?unary : "-" atom          -> neg 
       | "!" atom          -> not_ 
       | call "?"          -> opt 
       | call

// Chamada de funções
?call  : ID "(" xargs ")" 
       | attr

?xargs : expr ("," expr)*

// Acesso de atributos como em x.foo.bar.
?attr  : call ("." ID)+
       | ret

// Comandos de controle como return, continue, break.
// Permitidos apenas dentro de loops ou funções.
?ret   : "return" expr   -> ret
       | "continue"      -> loop_continue
       | "break"         -> loop_break
       | atom

?atom  : lit
       | "(" expr ")"

// Símbolos literais
lit    : INT
       | FLOAT
       | RESERVED
       | STRING
       | ID                -> name


// SÍMBOLOS TERMINAIS
//
// Você pode mudar estas regras, mas talvez seja necessário adaptar a regra de 
// "lit" no parser)

// Tipos inteiros
INT          : BIN_INT |  OCT_INT | HEX_INT | SIMPLE_INT
SIMPLE_INT   : /\d+((_)+\d*)*/
BIN_INT      : /0b(\d|_)+/ 
OCT_INT      : /0o(\d|_)+/ 
HEX_INT      : /0x(\d|\w|_)+/ 

// Tipos de ponto-flutante
FLOAT        : FLOAT_SCI | FLOAT_SIMPLE
FLOAT_SCI    : FLOAT_SIMPLE /[Ee][+-]?[0-9_]+/ | SIMPLE_INT /[Ee][+-]?[0-9_]+/
FLOAT_SIMPLE : /[0-9][0-9_]*\.([0-9][0-9_]*)?/

// Strings
STRING       : /.+/

// Nomes de variáveis, valores especiais
ID           : /x|y|z/
RESERVED     : /true|false|null/

// Comentários
COMMENT      : LINE_COMMENT | BLOCK_COMMENT
LINE_COMMENT : /\/{2}.*/
BLOCK_COMMENT: /\/\*.*\*\//

%ignore COMMENT
%ignore /\s+/
"""
grammar_expr = Lark(GRAMMAR, parser="lalr", start="seq")
grammar_mod = Lark(GRAMMAR, parser="lalr", start="mod")


# (não modifique o nome desta classe, fique livre para alterar as implementações!)
class RuspyTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow, neg, pos
    from operator import rshift, lshift, or_, and_, xor
    from operator import eq, ne, gt, lt, ge, le

    global_names = {
        **vars(math),  # Inclui todas funções do módulo math
        **vars(builtins),  # Inclui todas funções padrão do python
        "answer": 42,
        "println": print,
        "true": True,
        "false": False,
        "null": None,
    }

    # Estas declarações de tipo existem somente para deixar o VSCode feliz.
    _transform_children: Any
    _call_userfunc: Any
    transform: Any

    # Construtor
    def __init__(self):
        super().__init__()
        self.env = self.global_names.copy()

    # Trata símbolos terminais -------------------------------------------------
    def INT(self, tk):
        # Às vezes precisamos nos esforçar um pouquinho mais para obter o 
        # resultado que simplesmente fazer a conversão int(x)
        data = tk.replace('_', '')
        if set(data) == {'0'}:
            return 0
        if len(data) > 1:
          if data[1] == 'b':
            return int(data, 2)
          elif data[1] == 'o':
            return int(data, 8)
          elif data[1] == 'x':
            return int(data, 16)
        return int(data)

    def FLOAT(self, tk):
        data = tk.replace('_', '')
        return float(data)

    # Trata símbolos não-terminais ---------------------------------------------
    def lit(self, tk):
        if not isinstance(tk, Token):
            return tk
        try:
            return getattr(self, tk.type)(tk)
        except AttributeError:
            raise NotImplementedError(f"Implemente a regra def {tk.type}(self, tk): ... no transformer")

    def name(self, name):
        raise NotImplementedError("name")

    def assign(self, name, value):
        self.env[name] = value
        return self.env[name]

    ...

    # Formas especiais --------------------------------------------------------

    # Não-terminais normais recebem argumentos já transformados. As formas
    # especiais exigem a avaliação manual, o que pode ser útil para controlar
    # com mais precisão quantas vezes cada argumento deve ser avaliado. Isto é
    # útil em laços, execução condicional etc.
    #
    # A lista de formas especiais precisa ser declarada explicitamente
    special = {"if_", "for_", "while_", "fn", "lambd", "and_e", "or_e"}

    # Sobrescrevemos este método para habilitar formas especiais no transformer.
    def _transform_tree(self, tree):
        if tree.data in self.special:
            children = tree.children
        else:
            children = list(self._transform_children(tree.children))
        return self._call_userfunc(tree, children)

    # A avaliação é feita pelo método eval.
    def eval(self, obj):
        """
        Força a avaliação de um nó da árvore sintática em uma forma especial.
        """
        if isinstance(obj, Tree):
            return self.transform(obj)
        elif isinstance(obj, Token):
            try:
                return getattr(self, obj.type)(obj)
            except AttributeError:
                return obj
        else:
            return obj

    # Lista de formas especiais
    def and_e(self, x, y):
        # Esta é a forma mais simples. Avaliamos explicitamente cada argumento.
        # Note que "x and y" em Python avalia x e somente avalia y caso o primeiro
        # argumento seja verdadeiro. Este é exatamente o comportamento desejado.
        return self.eval(x) and self.eval(y)

    def or_e(self, x, y):
        return self.eval(x) or self.eval(y)

    def if_(self, cond, then, else_=None):
      if cond == true:
        return then
      else:
        return None

    def while_(self, cond, block):
        raise NotImplementedError("while")

    def for_(self, id, expr, block):
        raise NotImplementedError("for")

    def fn(self, name, args, block):
        # Dica: reaproveite a implementação de lambd
        raise NotImplementedError("fn")

    def lambd(self, args, block):
        raise NotImplementedError("fn")


def eval(src):
    """
    Avalia uma expressão ruspy.

    >>> eval("1 + 1")
    2
    """
    return _eval_or_exec(src, is_exec=False)


def module(src) -> dict:
    """
    Avalia um módulo ruspy e retorna um dicionário com as funções definidas
    no módulo.

    Você pode utilizar estas funções a partir de código Python.

    >>> dic = module("fn incr(n: int) { n + 1 }")
    >>> f = dic["incr"]
    >>> f(1)
    2
    """
    return _eval_or_exec(src, is_exec=True)


def run(src):
    """
    Avalia um módulo ruspy e executa automaticamente a função main.

    >>> src = '''
    ... fn main() {
    ...     print("hello world!")
    ... }
    ... '''
    hello world!
    """
    mod = module(src)
    main = mod.get("main")
    if not main:
        raise RuntimeError('módulo não define uma função "main()"')
    main()


def _eval_or_exec(src: str, is_exec=False) -> Any:
    # Função utilizada internamente por eval/module/run.
    if is_exec:
        grammar = grammar_mod
    else:
        grammar = grammar_expr
    try:

        tree = grammar.parse(src)
    except LarkError:
        print(f"Erro avaliando a expressão: \n{src}")
        print("\nImprimindo tokens")
        for i, tk in enumerate(grammar.lex(src), start=1):
            print(f" - {i}) {tk} ({tk.type})")
        raise
    transformer = RuspyTransformer()
    result = transformer.transform(tree)

    if isinstance(result, Tree):
        print(tree.pretty())
        bads = [*tree.find_pred(lambda x: not hasattr(transformer, x.data))]
        bad = bads[0] if bads else tree
        raise NotImplementedError(
            f"""
não implementou regra para lidar com: {tree.data!r}.
Crie um método como abaixo na classe do transformer.
    def {bad.data}(self, ...): 
        return ... 
"""
        )
    return result


# Interface de linha de comando. Lê um arquivo ruspy e passa para a função
# eval ou equivalente. Você pode modificar o conteúdo dentro do "if" para
# executar outros códigos de teste quando for rodar o arquivo. O exemplo abaixo
# fornece uma interface de linha de comando minimamente decente para interagir
# com o ruspy.
if __name__ == "__main__":
    if "--help" in sys.argv:
        print("Digite python ruspy.py [ARQUIVO] [--script]")
        print("")
        print("Opções:")
        print("  --help:")
        print("         mostra mensagem de ajuda")
        print("  --script:")
        print("         avalia como expressão no modo script, como se")
        print("         estivéssemos executando o código dentro da função main()")
        exit()
    elif "--script" in sys.argv:
        do_eval = True
        del sys.argv[sys.argv.index("--script")]
    else:
        do_eval = False
    with open(sys.argv[-1]) as fd:
        src = fd.read()
        if do_eval:
            print(f"\n> {eval(src)}")
        else:
            run(src)