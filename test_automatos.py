"""
Este arquivo mostra uma sequência de exercícios para provas as competências de
autômatos. A entrega destes exercícios será feita em um formulário específico 
onde seja possível subir arquivos com as respostas digitalizadas no formato pdf. 

Testaremos as habilidades abaixo

# [dfa-repr]

Entender o mecanismo de operação de um autônomo determinístico finito. 

* Definir autômato na forma gráfica e compreender o mecanismo de operação.
* Compreender a influência do estado inicial, alfabeto de entrada e estados de aceite na operação de um autômato.


# [nfa-repr]

Entender o mecanismo de operação de um autônomo não-determinístico finito. 

* Definir autômato na forma gráfica e compreender o mecanismo de operação.
* Compreender as diferenças de operação com relação a um autômato determinístico.
* Compreender a influência do estado inicial, alfabeto de entrada e estados de aceite na operação de um autômato.


# [nfa-thompson]

Criação de NFA para representação de Regex na construção de Thompson. 

* Compreender limitações da abordagem intuitiva.
* Entender a propriedade de composição da construção de Thompson.
* Realizar corretamente a construção de Thompson para expressões regulares arbitrárias.


# [nfa-epsilon]

Conversão de NFA-e para NFA. 

* Compreender que ambos possuem o mesmo poder computacional.
* Ser capaz de converter NFA-e para NFA sem transições epsilon


# [nfa-dfa]

Conversão de NFA para DFA. 

* Compreender que ambos possuem o mesmo poder computacional.
* Realizar a conversão de um NFA no DFA correspondente.indentificar
* Traduzir autômatos escritos como diagramas para código. 

----

Podemos abstrair a regra de aceitação de números inteiros simples em Ruspy
como sendo a expressão regular d(d|u)*, onde d representa os dígito e
u o underscore. O menor autômato determinístico finito (DFA) que representa
esta linguagem contêm apenas 2 estados. 

Com base nestas informações, responda

a) [dfa-repr] Desenhe um diagrama deste automato, destacando claramente o estado 
   inicial, os estados de aceite e as transições válidas.
b) [nfa-thompson] Crie a construção de Thompson para esta mesma linguagem. Observe
   que o resultado é um autômato consideravelmente maior na categoria NFA-e.
c) [nfa-epsilon] Elimine todas as transições epsilon do autômato da questão
    anterior.
d) [nfa-repr] Represente o autômato da questão anterior tanto como um 
   diagrama/grafo como pela tabela de transições correspondente.
e) [nfa-dfa] Termine a conversão do autômato da questão c para um DFA.
"""
