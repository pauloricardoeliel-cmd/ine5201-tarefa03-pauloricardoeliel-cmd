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


