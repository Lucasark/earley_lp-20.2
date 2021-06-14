[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=4510666&assignment_repo_type=AssignmentRepo)
# Algoritmo de reconhecimento de Earley

Christiano Braga

Trabalho do curso de Linguagens Formais e Teoria da Computação de 2020.2

Data de entrega: 07/05/2021

## Objetivo

Implementar em Python 3 o algoritmo de reconhecimento de Earley.

O programa deve receber uma gramática livre de contexto, uma palavra e identificar se a palavra dada pertence ou não a linguagem gerada pela gramática dada. Caso pertença, deve imprimir a árvore sintática associada a palavra dada. Caso contrário, deve mostrar em qual ponto da construção da derivação não foi possível continuar.

## Implementação

A implementação deste trabalho deve conter ao menos 2 módulos: `driver` e `earley`. O módulo `driver` deve conter a função `main`, o tratamento da linha de comando de chamada do programa e as chamadas às funções implementadas no módulo `earley`. 

A linha de comando da chamada do programa deverá receber dois parâmetros: (i) o nome de um arquivo texto contendo a descrição de uma gramática livre de contexto e (ii) a palavra a ser analisada, como por exemplo `python3 driver.py anbn.grm aabb`.

O módulo `earley` deve conter ao menos as seguintes funções:
1. `parse : GLC String -> Derivation`. Esta função recebe uma gramática livre de contexto, uma string, e retorna uma derivação.
1. `printDerivation : Derivation -> Tree`. Esta função recebe uma
   derivação e retorna uma árvore sintática, possivelmente mal-formada
   se a derivação for incompleta. O tipo `Tree` pode ser implementado
   completamente ou através de algum tipo existente em Python como um
   dicionário (com dicionários aninhados).
1. `parseGrm : String -> dict`. Esta função recebe uma string e retorna um dicionário representando a gramática descrita na string dada. A string deve ser da forma `V -> alpha`, onde `V` é uma variável (não-terminal) e alpha é uma palavra composta por símbolos variáveis e terminais separados por `.`. Por exemplo, a gramática `S -> a.S.b | epsilon` dá origem ao dicionário `{ "S" : [["a", "S", "b"], ["epsilon"]] }`. Produções podem ser separadas por quebra de linha, como por exemplo `S -> a.S.b\nS -> epsilon`.

## Execução

- Requirement:
```
$ pip3 install anytree –-user
```

- Chamada do programa:
```
$ python3 driver.py anbn.grm aabb
AnyNode(root='S')
├── AnyNode(root='a')
├── AnyNode(root='S')
│   ├── AnyNode(root='a')
│   └── AnyNode(root='b')
└── AnyNode(root='b')
```
