import openpyxl
import webbrowser
import pyautogui
from time import sleep
from urllib.parse import quote


webbrowser.open('https://web.whatsapp.com/')
sleep(30)
workbook = openpyxl.load_workbook('clientes.xlsx')
pagina_clientes = workbook['Planilha1']

for linha in pagina_clientes.iter_rows(min_row=2):
    nome = linha[0].value
    telefone = linha[1].value
    vencimento = linha[2].value
    mensagem = f'Olá {nome} seu boleto venceu no dia {vencimento.strftime("%d/%m/%Y")}. Favor pagar no link https://www.link.com.br'
    

    try:
        link_mensagem_whatsapp = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
        print(link_mensagem_whatsapp) 
        webbrowser.open(link_mensagem_whatsapp)
        sleep(10)
        seta = pyautogui.locateCenterOnScreen('seta.png')
        print(seta)
        sleep(2)
        pyautogui.click(seta[0],seta[1])
        sleep(2)
        pyautogui.hotkey('ctrl','w')
        sleep(2)
    except Exception as e:
        print(f'Não foi possível enviar mensagem para {nome}')
        with open('erros.csv','a',newline='', encoding='utf-8') as arquivo:
            arquivo.write(f'{nome},{telefone},{e}')

