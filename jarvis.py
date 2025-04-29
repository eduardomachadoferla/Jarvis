import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
import os
import webbrowser
import subprocess
import smtplib
import random
import json
from datetime import datetime, timedelta
from translate import Translator

# === CONFIGURAÇÕES ===
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
idioma = 'pt-BR'
wikipedia.set_lang('pt')

# OpenWeather API Key
API_WEATHER = "548a905eb36c4289a58ae41aebb453a3"

# Memoria de anotações e lembretes
arquivo_memoria = "lembretes.json"

# === FUNÇÕES BASE ===
def falar(texto):
    print(f"[Jarvis] {texto}")
    engine.say(texto)
    engine.runAndWait()

def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Escutando...")
        r.adjust_for_ambient_noise(fonte)
        audio = r.listen(fonte)
    try:
        comando = r.recognize_google(audio, language=idioma)
        print(f"Você disse: {comando}")
        return comando.lower()
    except:
        print("Não consegui entender.")
        return ""

# === FUNÇÕES EXTRAS ===
def buscar_wikipedia(termo):
    try:
        resultado = wikipedia.summary(termo, sentences=2)
        falar(resultado)
        salvar_anotacao(f"Wikipedia - {termo}", resultado)
    except:
        falar("Não encontrei resultados na Wikipedia.")

def falar_hora():
    agora = datetime.now()
    hora = agora.strftime("%H:%M")
    dia = agora.strftime("%d/%m/%Y")
    falar(f"Agora são {hora} de {dia}.")

def pegar_clima(cidade):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_WEATHER}&lang=pt_br&units=metric"
        resposta = requests.get(url).json()
        descricao = resposta['weather'][0]['description']
        temperatura = resposta['main']['temp']
        falar(f"O clima em {cidade} está {descricao} com {temperatura:.1f} graus.")
    except:
        falar("Não consegui obter o clima agora.")

def tocar_musica():
    falar("Qual música você quer ouvir?")
    musica = ouvir_comando()
    if musica:
        webbrowser.open(f"https://www.youtube.com/results?search_query={musica}")
        falar(f"Tocando {musica} no YouTube.")

def salvar_anotacao(titulo, conteudo):
    memoria = carregar_memoria()
    memoria[titulo] = conteudo
    with open(arquivo_memoria, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

def carregar_memoria():
    if os.path.exists(arquivo_memoria):
        with open(arquivo_memoria, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def contar_piadas():
    piadas = [
        "Por que o programador foi ao médico? Porque ele tinha um bug.",
        "O que o zero disse para o oito? Belo cinto!",
        "Qual é o rei dos queijos? O reiqueijão!"
    ]
    falar(random.choice(piadas))

def mudar_voz():
    falar("Deseja voz masculina ou feminina?")
    escolha = ouvir_comando()
    if "masculina" in escolha:
        for voz in voices:
            if "male" in voz.id.lower():
                engine.setProperty('voice', voz.id)
                falar("Voz masculina ativada.")
                return
    elif "feminina" in escolha:
        for voz in voices:
            if "female" in voz.id.lower():
                engine.setProperty('voice', voz.id)
                falar("Voz feminina ativada.")
                return
    falar("Não encontrei a voz solicitada.")

def traduzir_frase():
    falar("O que você quer traduzir?")
    frase = ouvir_comando()
    falar("Para qual idioma?")
    idioma_destino = ouvir_comando()
    tradutor = Translator(to_lang=idioma_destino)
    traducao = tradutor.translate(frase)
    falar(f"A tradução é: {traducao}")

def criar_lembrete():
    falar("Para qual dia é o lembrete? Pode dizer 'amanhã' ou uma data no formato dia barra mês.")
    data_str = ouvir_comando()
    hoje = datetime.now()

    if "amanhã" in data_str:
        data = hoje + timedelta(days=1)
    else:
        try:
            data = datetime.strptime(data_str, "%d/%m")
            data = data.replace(year=hoje.year)
        except:
            falar("Não entendi a data. Tente novamente dizendo por exemplo 'amanhã' ou '15 barra 08'.")
            return

    falar("O que você quer que eu te lembre nesse dia?")
    conteudo = ouvir_comando()

    memoria = carregar_memoria()
    data_formatada = data.strftime("%d/%m/%Y")

    if data_formatada not in memoria:
        memoria[data_formatada] = []

    memoria[data_formatada].append(conteudo)

    with open(arquivo_memoria, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)

    falar(f"Lembrete para {data_formatada} salvo com sucesso.")

def consultar_lembrete():
    falar("Para qual dia você quer ver a sua agenda?")
    data_str = ouvir_comando()

    hoje = datetime.now()
    if "amanhã" in data_str:
        data = hoje + timedelta(days=1)
    else:
        try:
            data = datetime.strptime(data_str, "%d/%m")
            data = data.replace(year=hoje.year)
        except:
            falar("Não entendi a data. Tente novamente.")
            return

    data_formatada = data.strftime("%d/%m/%Y")
    memoria = carregar_memoria()

    if data_formatada in memoria and memoria[data_formatada]:
        falar(f"Você tem {len(memoria[data_formatada])} lembrete(s) para {data_formatada}:")
        for item in memoria[data_formatada]:
            falar(item)
    else:
        falar(f"Você não tem nem um agendamento para {data_formatada}.")

def enviar_email():
    try:
        falar("Qual o email do destinatário?")
        destinatario = ouvir_comando()
        falar("Qual o assunto?")
        assunto = ouvir_comando()
        falar("Qual a mensagem?")
        mensagem = ouvir_comando()

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(EMAIL, SENHA)
        corpo = f"Subject: {assunto}\n\n{mensagem}"
        servidor.sendmail(EMAIL, destinatario, corpo.encode('utf-8'))
        servidor.quit()
        falar("Email enviado com sucesso.")
    except Exception as e:
        print(e)
        falar("Não consegui enviar o email.")

def abrir_aplicativo():
    falar("Qual aplicativo deseja abrir?")
    app = ouvir_comando()
    if "calculadora" in app:
        subprocess.Popen('calc.exe')
    elif "navegador" in app:
        webbrowser.open('https://www.google.com')
    else:
        falar("Não reconheci o aplicativo.")

# === FUNÇÃO PRINCIPAL ===
def main():
    falar("Assistente iniciado. Diga 'Ei Jarvis', para começar.")

    ativacoes = ["ei jarvis", "ei jair", "hey jarvis", "hey jair", "ei jar", "hey jar", "ei jaris", "e aí jarvis"]

    while True:
        comando = ouvir_comando()

        if any(ativacao in comando for ativacao in ativacoes):
            falar("Estou ouvindo! Como posso ajudar?")
            while True:
                comando = ouvir_comando()

                if comando == "":
                    continue

                if "sair" in comando:
                    falar("Até logo!")
                    break
                elif "hora" in comando:
                    falar_hora()
                elif "clima em""tempo" in comando:
                    cidade = comando.replace("clima em", "").strip()
                    pegar_clima(cidade)
                elif "tocar música" in comando:
                    tocar_musica()
                elif "anotar" in comando:
                    falar("O que deseja anotar?")
                    nota = ouvir_comando()
                    salvar_anotacao(f"Anotação - {datetime.now()}", nota)
                    falar("Anotação salva.")
                elif "conte uma piada" in comando:
                    contar_piadas()
                elif "mudar voz" in comando:
                    mudar_voz()
                elif "traduzir" in comando:
                    traduzir_frase()
                elif "criar lembrete" in comando:
                    criar_lembrete()
                elif "ver agenda" in comando or "minha agenda" in comando:
                    consultar_lembrete()
                elif "enviar email" in comando:
                    enviar_email()
                elif "abrir" in comando:
                    abrir_aplicativo()
                elif "o que é" in comando or "quem é" in comando:
                    termo = comando.replace("o que é", "").replace("quem é", "").strip()
                    buscar_wikipedia(termo)
                else:
                    falar("Não entendi. Pode repetir?")
        elif "obrigado" in comando:
            falar("imagina denada qualquer coisa estou a sua dispociçao")
            break

if __name__ == "__main__":
    main()
