Execução do programa:

    O programa está escrito na linguagem "Python" e está todo contido no arquivo
'main.py'. Para executá-lo, basta executar:

> python main.py

ou qualquer outro método de execução de arquivos python com suporte para entrada 
de dados pelo teclado.

    Para melhor performance na execução, é recomendado utilizar a implementação
da linguagem Python "pypy", apesar de não ser obrigatório para a execução do código.

    Em caso de uso do "pypy", a execução é semelhante a uma execução python regular:

> pypy main.py

link para o compilador pypy -> https://www.pypy.org/

OBS: o tempo de execução do relatório é baseado na execução da implementação oficial
do Python e não do pypy.

Entradas:

    O código tem alguns testes pré-implementados a escolha do usuário, basta selecionar a
opção desejada no terminal.
    Tenha em mente que algumas opções precisam da entrada de nomes de arquivos e/ou número de iterações, e
se faz necessário ou definir o caminho até o arquivo com sua devida extensão (.txt, .dat, etc).
    Relembrar também que o formato dos dados de entrada devem ser da seguinte maneira:

(label) <numero-de-linhas>
(label) <numero-de-colunas>
(label)
<indice-da-coluna> <custo-da-coluna> <linha-coberta> <linha-coberta> ...
<indice-da-coluna> <custo-da-coluna> <linha-coberta> <linha-coberta> ...
...