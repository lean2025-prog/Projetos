import FreeSimpleGUI as sg
import copy
sg.theme('darkblue3')
def obter_ordem():
    layout1 = [[sg.Text('Digite a ordem da matriz quadrada (de 1 a 4):')],
               [sg.Input(key='-ordem_da_matriz-',size=(5,1))],
               [sg.Button('Confirmar'),sg.Button('Sair')]]
    janela1 = sg.Window('Calculadora de Determinante', layout1, enable_close_attempted_event=True)
    while True:
        event, value = janela1.read()
        if event in ('Sair', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            conf = sg.popup_yes_no('Quer mesmo sair do programa?', no_titlebar=True)
            if conf == 'Yes':
                return None
        if event == 'Confirmar':
            try:
                ordem_int = int(value['-ordem_da_matriz-'])
                if 0 < ordem_int <= 4:
                    janela1.close()
                    return ordem_int
                else:
                    sg.popup_error('ERRO! Digite um número inteiro (de 1 a 4)!', no_titlebar=True)
            except ValueError:
                sg.popup_error('ERRO! Digite um número inteiro (de 1 a 4)!', no_titlebar=True)
def obter_matriz(ordem_int):
    layout2 = [[sg.Text(f'Digite os elementos da matriz quadrada de ordem {ordem_int} X {ordem_int}:')]]
    for linha in range(ordem_int):
        linha_widget = []
        for coluna in range(ordem_int):
            linha_widget.append(sg.Input(key=f'-linha{linha}-coluna{coluna}-',size=(8,1)))
        layout2.append(linha_widget)
    layout2.append([sg.Button('Calcular determinante'),sg.Button('Cancelar')])
    janela2 = sg.Window('Digite os elementos da matriz:', layout2, enable_close_attempted_event=True)
    while True:
        event, value = janela2.read()
        if event in ('Cancelar', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            conf2 = sg.popup_yes_no('Quer mesmo sair do programa?', no_titlebar=True)
            if conf2 == 'Yes':
                janela2.close()
                return None
        if event == 'Calcular determinante':
            matriz = []
            try:
                for linha in range(ordem_int):
                    linha_valores = []
                    for coluna in range(ordem_int):
                        valor = float(value[f'-linha{linha}-coluna{coluna}-'].replace(',', '.'))
                        linha_valores.append(valor)
                    matriz.append(linha_valores)
                janela2.close()
                return matriz
            except ValueError:
                sg.popup_error('ERRO! Todos os elementos da matriz devem ser números (inteiros ou decimais)!', no_titlebar=True)
def calcular_determinante_e_triangular(matriz_original_param):
    determinante = None
    mensagem_erro = None
    matriz_triangulada = []
    temp_matriz = copy.deepcopy(matriz_original_param)
    n = len(temp_matriz)
    trocas_de_linha = 0
    try:
        for i in range(n):
            if abs(temp_matriz[i][i]) < 1e-9:
                pivo_encontrado = False
                for k in range(i + 1, n):
                    if abs(temp_matriz[k][i]) >= 1e-9:
                        temp_matriz[i], temp_matriz[k] = temp_matriz[k], temp_matriz[i]
                        trocas_de_linha += 1
                        pivo_encontrado = True
                        break
                if not pivo_encontrado:
                    determinante = 0.0
                    matriz_triangulada = copy.deepcopy(temp_matriz)
                    return matriz_original_param, matriz_triangulada, determinante, "Determinante: 0.0 (Matriz Singular)"
            for j in range(i + 1, n):
                if abs(temp_matriz[i][i]) < 1e-9:
                    continue 
                fator = temp_matriz[j][i] / temp_matriz[i][i]
                for k in range(i, n):
                    temp_matriz[j][k] -= fator * temp_matriz[i][k]
        determinante = 1.0
        for i in range(n):
            determinante *= temp_matriz[i][i]
        if trocas_de_linha % 2 == 1:
            determinante *= -1
        matriz_triangulada = copy.deepcopy(temp_matriz)
        return matriz_original_param, matriz_triangulada, determinante, None
    except Exception as e:
        mensagem_erro = f"Ocorreu um erro inesperado durante o cálculo: {e}"
    return matriz_original_param, matriz_triangulada, determinante, mensagem_erro
def formatar_matriz_para_exibicao(matriz):
    if not matriz:
        return "Matriz vazia ou inválida."
    
    num_cols = len(matriz[0])
    larguras_colunas = [0] * num_cols
    for linha in matriz:
        for j, elemento in enumerate(linha):
            larguras_colunas[j] = max(larguras_colunas[j], len(f"{elemento:.2f}"))
    saida = []
    for linha in matriz:
        linha_formatada = []
        for j, elemento in enumerate(linha):
            linha_formatada.append(f"{elemento:.2f}".rjust(larguras_colunas[j]))
        saida.append(f"[ {' '.join(linha_formatada)} ]")
    return "\n".join(saida)
if __name__ == '__main__':
    ordem = obter_ordem()
    if ordem is not None:
        matriz_original = obter_matriz(ordem)
        if matriz_original is not None:
            matriz_original_exibir, matriz_triangulada_exibir, determinante_final, erro_calculo = \
                calcular_determinante_e_triangular(matriz_original)
            if erro_calculo:
                sg.popup_error('Erro no Cálculo', erro_calculo, no_titlebar=True)
            else:
                layout_resultado = [
                    [sg.Text("Resultados do Cálculo do Determinante", font=("Arial", 15, "bold"), expand_x=True, justification='center')],
                    [sg.HorizontalSeparator()],
                    [sg.Column([
                        [sg.Text("Matriz Original:", font=("Arial", 12, "bold"))],
                        [sg.Multiline(default_text=formatar_matriz_para_exibicao(matriz_original_exibir), 
                                     size=(30, ordem + 2), disabled=True, font=("Courier New", 11), 
                                     no_scrollbar=True)],
                    ], vertical_alignment='top', element_justification='center'),
                    sg.Column([
                        [sg.Text("Matriz Triangulada:", font=("Arial", 12, "bold"))],
                        [sg.Multiline(default_text=formatar_matriz_para_exibicao(matriz_triangulada_exibir), 
                                     size=(30, ordem + 2), disabled=True, font=("Courier New", 11), 
                                     no_scrollbar=True)],
                    ], vertical_alignment='top', element_justification='center')],
                    [sg.HorizontalSeparator()],
                    [sg.Text(f"Determinante Final: {determinante_final:.2f}", 
                             font=("Arial", 14, "bold"), text_color='white',
                             expand_x=True, justification='center')],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Explicação do Método de Triangulação:", font=("Arial", 12, "bold"))],
                    [sg.Multiline(
                        "O determinante é calculado através da **triangulação da matriz**.\n"
                        "1. A matriz original é transformada em uma **matriz triangular superior**, onde todos os elementos abaixo da diagonal principal se tornam zero.\n"
                        "2. Isso é feito usando **operações elementares de linha**: multiplicar uma linha por um escalar e somá-la a outra.\n"
                        "3. O determinante da matriz triangular é simplesmente o **produto dos elementos na sua diagonal principal**.\n"
                        ,
                        size=(60, 10), disabled=True, font=("Arial", 10), no_scrollbar=True)],
                    [sg.Button("Fechar", font=("Arial", 11), button_color=('white', 'red'), key='-FECHAR_RESULTADOS-')]
                ]
                janela_resultados = sg.Window("Resultados do Determinante", layout_resultado, modal=True, resizable=False)
                while True:
                    event_resultado, values_resultado = janela_resultados.read()
                    if event_resultado == sg.WIN_CLOSED or event_resultado == '-FECHAR_RESULTADOS-':
                        break
                janela_resultados.close()
                print(4)