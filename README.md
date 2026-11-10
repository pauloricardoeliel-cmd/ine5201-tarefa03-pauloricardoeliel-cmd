# Jogo da Forca

Tarefa 03 da disciplina **INE5201 - Introdução à Ciência da Computação com Python** (UFSC).

Jogo da Forca com interface gráfica em FreeSimpleGUI. As palavras são lidas do arquivo `palavras.txt` e sorteadas a cada partida, o boneco é desenhado parte por parte a cada erro e as estatísticas de vitórias e derrotas ficam salvas entre uma execução e outra.

## Participantes

| Nome | Matrícula |
|---|---|
| Paulo Ricardo Eliel Mendes Peres dos Santos | 24100434 |
| Matheus da Silva Farani | 24202994 |

## Como executar

Requisito: Python 3.10 ou mais recente.

```bash
pip install -r requirements.txt
python forca_gui.py
```

No Windows, se `python` não for reconhecido, use `py` no lugar. O arquivo `palavras.txt` precisa estar na mesma pasta do `forca_gui.py`.

## Como jogar

Uma palavra é sorteada e aparece com as letras ocultas (`_ _ _ _`). Clique nas letras do teclado virtual ou digite no teclado do computador. Cada letra certa aparece na palavra e fica verde. Cada letra errada fica vermelha e desenha uma parte do boneco. Vence quem descobrir a palavra antes de 6 erros.

| Botão | O que faz |
|---|---|
| **Novo Jogo** | Sorteia outra palavra. Se a partida atual já começou, ela conta como derrota (o jogo pergunta antes). |
| **Desistir** | Encerra a partida como derrota e revela a palavra. |
| **Dica** | Revela uma letra oculta ao custo de 1 tentativa. Pode ser usada uma vez por partida e só quando resta mais de uma tentativa. |

## Funcionalidades

**Interface**
- Palavra com letras ocultas no formato `P _ T H _ N`
- Teclado virtual de A a Z; as letras já usadas ficam desabilitadas, em verde (acerto) ou vermelho (erro)
- Forca e boneco desenhados em um `sg.Graph`, com 6 partes: cabeça, tronco, 2 braços e 2 pernas
- Contador de tentativas restantes e lista das letras erradas
- Mensagens de acerto, erro, vitória e derrota na janela e em popup
- Botões **Novo Jogo**, **Desistir** e **Dica**
- Placar com vitórias, derrotas, total de partidas e aproveitamento

**Regras e validações**
- Máximo de 6 erros
- Letra repetida não conta como erro: aparece o aviso "A letra X já foi tentada"
- Ao perder ou desistir, a palavra inteira é revelada
- A nova palavra nunca é igual à da partida anterior
- Depois do fim da partida, o teclado fica bloqueado até clicar em **Novo Jogo**

**Arquivos e strings**
- `palavras.txt` com 64 palavras, uma por linha
- Na leitura, cada linha passa por `strip()`, tem os acentos removidos e vai para maiúsculas: `coração` vira `CORACAO`
- Linhas vazias, comentários (`#`), palavras repetidas e linhas com números ou símbolos são ignoradas
- Se o arquivo não existir ou tiver menos de 50 palavras válidas, o jogo mostra uma mensagem de erro em vez de travar
- As estatísticas ficam em `estatisticas.txt`, no formato `vitorias=3`; se o arquivo estiver corrompido, a contagem recomeça do zero

## Estrutura do código

```
forca_gui.py
├── Constantes: caminhos dos arquivos, limites, alfabeto e cores
├── Arquivos
│   ├── normalizar(texto)
│   ├── carregar_palavras(arquivo)
│   ├── escolher_palavra(lista, anterior)
│   ├── carregar_estatisticas()
│   └── salvar_estatisticas(vitorias, derrotas)
├── Lógica do jogo
│   ├── atualizar_display(palavra, letras_tentadas)
│   ├── verificar_vitoria(palavra, letras_tentadas)
│   ├── letras_erradas(palavra, letras_tentadas)
│   ├── contar_erros(estado)
│   ├── tentar_letra(estado, letra)
│   ├── revelar_dica(estado)
│   └── novo_estado(palavras, anterior)
├── Interface gráfica
│   ├── desenhar_boneco(grafico, erros)
│   ├── criar_layout()
│   ├── atualizar_tela(window, estado, mensagem, cor)
│   ├── encerrar_partida(window, estado, estatisticas, venceu, mensagem)
│   ├── processar_letra(window, estado, estatisticas, letra)
│   └── letra_do_evento(event)
└── main(): carrega os arquivos e roda o loop de eventos
palavras.txt: 64 palavras, uma por linha
```

**Estado da partida.** Tudo que muda durante uma partida fica em um dicionário: a palavra sorteada, o conjunto (`set`) de letras tentadas e quantas dicas foram usadas. Com um `set`, verificar se uma letra já foi tentada é só `letra in tentadas`, e a vitória é `set(palavra) <= tentadas`, ou seja, todas as letras da palavra já foram tentadas.

**Erros contados a partir das letras.** O número de erros não é guardado em uma variável separada: ele é calculado como a quantidade de letras tentadas que não estão na palavra, mais as dicas usadas. Assim o contador e o desenho nunca ficam fora de sincronia.

**Remoção de acentos.** `normalizar` usa `unicodedata.normalize('NFD', ...)`, que separa cada letra do seu acento (`ã` vira `a` + `~`), e depois descarta os acentos. Por isso o arquivo pode ter palavras acentuadas e o jogador só precisa das letras de A a Z.

**Caminho dos arquivos.** Os arquivos são localizados a partir da pasta do próprio `forca_gui.py` (`os.path.dirname(__file__)`), então o jogo funciona mesmo se for executado de outra pasta.

## Screenshots

**Partida em andamento**

![Partida em andamento](screenshots/partida.png)

**Vitória**

![Vitória](screenshots/vitoria.png)

**Derrota com o boneco completo**

![Derrota](screenshots/derrota.png)

## Uso do GitHub Copilot

<!-- PREENCHER com o que vocês realmente fizeram no VS Code. -->

| Prompt | Função assistida | O que aproveitei ou mudei |
|---|---|---|
| "..." | | |
| "..." | | |
| "..." | | |

**Relato.** <!-- Um parágrafo: em quais funções o Copilot ajudou, uma sugestão aceita, uma corrigida ou descartada e por quê. -->

## Tecnologias

- Python 3
- [FreeSimpleGUI](https://pypi.org/project/FreeSimpleGUI/)
- Bibliotecas padrão: `random`, `os` e `unicodedata`
- GitHub Copilot
