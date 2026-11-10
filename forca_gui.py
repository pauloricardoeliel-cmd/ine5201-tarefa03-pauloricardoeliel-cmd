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


