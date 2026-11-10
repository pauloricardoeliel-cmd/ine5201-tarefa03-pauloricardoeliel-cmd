"""
Jogo da Forca com interface gráfica
INE5201 - Introdução à Ciência da Computação com Python - UFSC
Tarefa 03

Participantes:
    Paulo Ricardo Eliel Mendes Peres dos Santos (24100434)
    Matheus da Silva Farani (24202994)

Como jogar:
    Clique nas letras do teclado virtual (ou digite no teclado) para
    adivinhar a palavra sorteada. Cada letra errada desenha uma parte
    do boneco; com 6 erros a partida está perdida.
"""

import os
import random
import unicodedata

import FreeSimpleGUI as sg

# ============================== Constantes ==============================

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_PALAVRAS = os.path.join(PASTA, 'palavras.txt')
ARQUIVO_ESTATISTICAS = os.path.join(PASTA, 'estatisticas.txt')

MAX_ERROS = 6           # cabeça, tronco, 2 braços e 2 pernas
MIN_PALAVRAS = 50       # mínimo exigido no arquivo
ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LINHAS_TECLADO = ['ABCDEFGHI', 'JKLMNOPQR', 'STUVWXYZ']

# Desenho (em pixels)
LARGURA_DESENHO = 260
ALTURA_DESENHO = 300

# Cores
COR_FUNDO_DESENHO = '#F4F1E8'
COR_FORCA = '#6B4226'
COR_BONECO = '#222222'
COR_ACERTO = ('#FFFFFF', '#27AE60')     # (texto, fundo) de letra certa
COR_ERRO = ('#FFFFFF', '#C0392B')       # (texto, fundo) de letra errada
COR_LETRA = ('#000000', '#E0E0E0')      # letra ainda não tentada
COR_VITORIA = '#27AE60'
COR_DERROTA = '#E74C3C'
COR_AVISO = '#F39C12'


# ============================== Arquivos ==============================

def normalizar(texto):
    """Tira acentos e espaços e passa para maiúsculas: ' Coração ' -> 'CORACAO'.

    unicodedata separa cada letra do seu acento (NFD); depois
    descartamos os acentos, que são da categoria 'Mn'.
    """
    decomposto = unicodedata.normalize('NFD', texto.strip())
    sem_acento = ''.join(c for c in decomposto if unicodedata.category(c) != 'Mn')
    return sem_acento.upper()


def carregar_palavras(arquivo):
    """Lê o arquivo e devolve a lista de palavras válidas, sem repetições.

    Ignora linhas vazias, comentários (#) e linhas com algo além de letras.
    Lança FileNotFoundError se o arquivo não existir e ValueError se
    houver menos de MIN_PALAVRAS palavras válidas.
    """
    palavras = []
    with open(arquivo, encoding='utf-8') as f:
        for linha in f:
            palavra = normalizar(linha)
            if not palavra or palavra.startswith('#'):
                continue
            if all(letra in ALFABETO for letra in palavra) and palavra not in palavras:
                palavras.append(palavra)

    if len(palavras) < MIN_PALAVRAS:
        raise ValueError(f'O arquivo tem só {len(palavras)} palavras válidas; '
                         f'o mínimo é {MIN_PALAVRAS}.')
    return palavras


def escolher_palavra(lista, anterior=''):
    """Sorteia uma palavra, evitando repetir a da partida anterior."""
    opcoes = [p for p in lista if p != anterior]
    return random.choice(opcoes)


def carregar_estatisticas():
    """Lê vitórias e derrotas salvas. Se o arquivo não existir ou estiver
    corrompido, começa do zero."""
    estatisticas = {'vitorias': 0, 'derrotas': 0}
    try:
        with open(ARQUIVO_ESTATISTICAS, encoding='utf-8') as f:
            for linha in f:
                chave, valor = linha.strip().split('=')
                if chave in estatisticas:
                    estatisticas[chave] = int(valor)
    except (FileNotFoundError, ValueError):
        pass
    return estatisticas


def salvar_estatisticas(vitorias, derrotas):
    """Grava as estatísticas no formato 'chave=valor', uma por linha."""
    with open(ARQUIVO_ESTATISTICAS, 'w', encoding='utf-8') as f:
        f.write(f'vitorias={vitorias}\n')
        f.write(f'derrotas={derrotas}\n')


# ============================== Lógica do jogo ==============================

def atualizar_display(palavra, letras_tentadas):
    """Monta o texto da palavra com as letras não descobertas ocultas.

    Exemplo: atualizar_display('PYTHON', {'P', 'O'}) -> 'P _ _ _ O _'
    """
    return ' '.join(letra if letra in letras_tentadas else '_' for letra in palavra)


def verificar_vitoria(palavra, letras_tentadas):
    """Vence quando todas as letras da palavra já foram tentadas."""
    return set(palavra) <= letras_tentadas


def letras_erradas(palavra, letras_tentadas):
    """Letras tentadas que não estão na palavra, em ordem alfabética."""
    return sorted(letra for letra in letras_tentadas if letra not in palavra)


def contar_erros(estado):
    return len(letras_erradas(estado['palavra'], estado['tentadas'])) + estado['dicas_usadas']


def tentar_letra(estado, letra):
    """Registra uma tentativa e devolve 'repetida', 'acerto' ou 'erro'."""
    if letra in estado['tentadas']:
        return 'repetida'
    estado['tentadas'].add(letra)
    return 'acerto' if letra in estado['palavra'] else 'erro'


def revelar_dica(estado):
    """Revela uma letra oculta ao custo de uma tentativa.

    Devolve a letra revelada, ou None se a dica não puder ser usada
    (já usada nesta partida ou só resta uma tentativa).
    """
    ocultas = [l for l in set(estado['palavra']) if l not in estado['tentadas']]
    if estado['dicas_usadas'] >= 1 or MAX_ERROS - contar_erros(estado) <= 1 or not ocultas:
        return None
    letra = random.choice(ocultas)
    estado['tentadas'].add(letra)
    estado['dicas_usadas'] += 1
    return letra


def novo_estado(palavras, anterior=''):
    return {
        'palavra': escolher_palavra(palavras, anterior),
        'tentadas': set(),
        'dicas_usadas': 0,
        'ativo': True,          # False depois de vitória, derrota ou desistência
        'revelada': False,      # True para mostrar a palavra inteira ao perder
    }


# ============================== Interface gráfica ==============================

def desenhar_boneco(grafico, erros):
    """Desenha a forca e as partes do boneco de acordo com o número de erros."""
    grafico.erase()
    # Forca: base, poste, travessa e corda
    grafico.draw_line((20, 285), (180, 285), color=COR_FORCA, width=8)
    grafico.draw_line((60, 285), (60, 20), color=COR_FORCA, width=8)
    grafico.draw_line((56, 20), (190, 20), color=COR_FORCA, width=8)
    grafico.draw_line((60, 60), (100, 20), color=COR_FORCA, width=5)
    grafico.draw_line((190, 20), (190, 55), color=COR_FORCA, width=3)

    partes = [
        lambda: grafico.draw_circle((190, 80), 25, line_color=COR_BONECO, line_width=4),
        lambda: grafico.draw_line((190, 105), (190, 185), color=COR_BONECO, width=4),
        lambda: grafico.draw_line((190, 125), (155, 160), color=COR_BONECO, width=4),
        lambda: grafico.draw_line((190, 125), (225, 160), color=COR_BONECO, width=4),
        lambda: grafico.draw_line((190, 185), (160, 240), color=COR_BONECO, width=4),
        lambda: grafico.draw_line((190, 185), (220, 240), color=COR_BONECO, width=4),
    ]
    for parte in partes[:erros]:
        parte()


def criar_layout():
    teclado = [[sg.Button(letra, key=f'-LETRA-{letra}', size=(3, 1),
                          font=('Helvetica', 14, 'bold'), button_color=COR_LETRA,
                          pad=(2, 2))
                for letra in linha]
               for linha in LINHAS_TECLADO]

    coluna_jogo = [
        [sg.Text('', key='-PALAVRA-', font=('Consolas', 30, 'bold'),
                 size=(26, 1), justification='center')],
        [sg.Text('', key='-TENTATIVAS-', font=('Helvetica', 14, 'bold'))],
        [sg.Text('', key='-ERRADAS-', font=('Helvetica', 12), text_color=COR_DERROTA,
                 size=(40, 1))],
        [sg.Text('', key='-MENSAGEM-', font=('Helvetica', 14, 'bold'), size=(40, 2))],
        *[[sg.Column([linha], pad=(0, 0))] for linha in teclado],
        [sg.Button('Novo Jogo', key='-NOVO-', size=(11, 1)),
         sg.Button('Desistir', key='-DESISTIR-', size=(11, 1)),
         sg.Button('Dica', key='-DICA-', size=(11, 1))],
        [sg.Text('', key='-ESTATISTICAS-', font=('Helvetica', 11))],
    ]

    return [
        [sg.Text('JOGO DA FORCA', font=('Helvetica', 24, 'bold'),
                 justification='center', expand_x=True)],
        [sg.Graph((LARGURA_DESENHO, ALTURA_DESENHO), (0, ALTURA_DESENHO),
                  (LARGURA_DESENHO, 0), background_color=COR_FUNDO_DESENHO,
                  key='-DESENHO-'),
         sg.Column(coluna_jogo, element_justification='center')],
    ]


def mostrar_estatisticas(window, estatisticas):
    v, d = estatisticas['vitorias'], estatisticas['derrotas']
    total = v + d
    aproveitamento = f'{100 * v / total:.0f}%' if total else '-'
    window['-ESTATISTICAS-'].update(
        f'Vitórias: {v}   Derrotas: {d}   Partidas: {total}   Aproveitamento: {aproveitamento}')


def atualizar_tela(window, estado, mensagem='', cor=None):
    """Redesenha palavra, boneco, contador, letras erradas e teclado."""
    palavra, tentadas = estado['palavra'], estado['tentadas']
    erros = contar_erros(estado)

    visiveis = tentadas | set(palavra) if estado['revelada'] else tentadas
    window['-PALAVRA-'].update(atualizar_display(palavra, visiveis))
    window['-TENTATIVAS-'].update(f'Tentativas restantes: {MAX_ERROS - erros}')
    erradas = letras_erradas(palavra, tentadas)
    window['-ERRADAS-'].update('Letras erradas: ' + ' '.join(erradas) if erradas else '')
    window['-MENSAGEM-'].update(mensagem, text_color=cor)
    desenhar_boneco(window['-DESENHO-'], erros)

    for letra in ALFABETO:
        botao = window[f'-LETRA-{letra}']
        if letra in tentadas:
            botao.update(disabled=True, button_color=COR_ACERTO if letra in palavra else COR_ERRO)
        else:
            botao.update(disabled=not estado['ativo'], button_color=COR_LETRA)

    window['-DESISTIR-'].update(disabled=not estado['ativo'])
    window['-DICA-'].update(disabled=not estado['ativo'] or estado['dicas_usadas'] >= 1)


def encerrar_partida(window, estado, estatisticas, venceu, mensagem):
    """Finaliza a partida, revela a palavra e salva as estatísticas."""
    estado['ativo'] = False
    if venceu:
        estatisticas['vitorias'] += 1
        cor = COR_VITORIA
    else:
        estatisticas['derrotas'] += 1
        estado['revelada'] = True
        cor = COR_DERROTA
    salvar_estatisticas(estatisticas['vitorias'], estatisticas['derrotas'])
    atualizar_tela(window, estado, mensagem, cor)
    mostrar_estatisticas(window, estatisticas)
    window.refresh()
    sg.popup(mensagem, 'Clique em "Novo Jogo" para jogar de novo.',
             title='Fim de jogo', keep_on_top=True)


def processar_letra(window, estado, estatisticas, letra):
    if not estado['ativo']:
        return
    resultado = tentar_letra(estado, letra)

    if resultado == 'repetida':
        atualizar_tela(window, estado, f'A letra {letra} já foi tentada.', COR_AVISO)
    elif verificar_vitoria(estado['palavra'], estado['tentadas']):
        encerrar_partida(window, estado, estatisticas, True,
                         f'Parabéns, você acertou: {estado["palavra"]}!')
    elif contar_erros(estado) >= MAX_ERROS:
        encerrar_partida(window, estado, estatisticas, False,
                         f'Você perdeu! A palavra era {estado["palavra"]}.')
    elif resultado == 'acerto':
        atualizar_tela(window, estado, f'Boa! A palavra tem a letra {letra}.', COR_VITORIA)
    else:
        atualizar_tela(window, estado, f'A palavra não tem a letra {letra}.', COR_DERROTA)


def letra_do_evento(event):
    """Converte o clique no teclado virtual ou uma tecla física em letra."""
    if not isinstance(event, str):
        return None
    if event.startswith('-LETRA-'):
        return event[-1]
    if len(event) == 1 and normalizar(event) in ALFABETO:
        return normalizar(event)
    return None


# ============================== Programa principal ==============================

def main():
    sg.theme('DarkTeal9')

    try:
        palavras = carregar_palavras(ARQUIVO_PALAVRAS)
    except FileNotFoundError:
        sg.popup_error(f'Arquivo não encontrado:\n{ARQUIVO_PALAVRAS}', title='Erro')
        return
    except ValueError as erro:
        sg.popup_error(str(erro), title='Erro no arquivo de palavras')
        return

    estatisticas = carregar_estatisticas()
    window = sg.Window('INE5201 - Jogo da Forca', criar_layout(), finalize=True,
                       return_keyboard_events=True)
    estado = novo_estado(palavras)
    atualizar_tela(window, estado, f'{len(palavras)} palavras carregadas. Boa sorte!')
    mostrar_estatisticas(window, estatisticas)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-NOVO-':
            if estado['ativo'] and estado['tentadas']:
                resposta = sg.popup_yes_no('A partida atual conta como derrota. Continuar?',
                                           title='Novo jogo')
                if resposta != 'Yes':
                    continue
                encerrar_partida(window, estado, estatisticas, False,
                                 f'Partida abandonada. A palavra era {estado["palavra"]}.')
            estado = novo_estado(palavras, estado['palavra'])
            atualizar_tela(window, estado, 'Nova palavra sorteada!')
            continue

        if event == '-DESISTIR-' and estado['ativo']:
            encerrar_partida(window, estado, estatisticas, False,
                             f'Você desistiu. A palavra era {estado["palavra"]}.')
            continue

        if event == '-DICA-' and estado['ativo']:
            letra = revelar_dica(estado)
            if letra is None:
                atualizar_tela(window, estado,
                               'Dica indisponível: só resta uma tentativa.', COR_AVISO)
            elif verificar_vitoria(estado['palavra'], estado['tentadas']):
                encerrar_partida(window, estado, estatisticas, True,
                                 f'Parabéns, você acertou: {estado["palavra"]}!')
            else:
                atualizar_tela(window, estado,
                               f'Dica: a palavra tem a letra {letra} (custou 1 tentativa).',
                               COR_AVISO)
            continue

        letra = letra_do_evento(event)
        if letra is not None:
            processar_letra(window, estado, estatisticas, letra)

    window.close()


if __name__ == '__main__':
    main()
