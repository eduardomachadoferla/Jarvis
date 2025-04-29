

# Jarvis

**Jarvis** é um assistente virtual controlado por voz, desenvolvido em Python, que entende comandos em português e realiza tarefas como:
- Consultar informações na Wikipedia  
- Informar o horário e o dia atual  
- Buscar o clima de uma cidade em tempo real  
- Criar lembretes com data específica  
- Consultar lembretes salvos para qualquer dia  
- Aprender novos comandos com o usuário através de uma memória persistente.

## Funcionalidades

✅ Reconhecimento de voz (speech recognition)  
✅ Resposta por voz (pyttsx3) com voz masculina em português  
✅ Consulta de informações (Wikipedia API)  
✅ Clima em tempo real (OpenWeather API)  
✅ Criação e consulta de lembretes por data (com suporte a "amanhã")  
✅ Ativação por voz com tolerância a variações de "Ei Jarvis"  
✅ Memorização de novos comandos  
✅ Interface totalmente em português 🇧🇷  

## Tecnologias usadas

- Python 3  
- [speech_recognition](https://pypi.org/project/SpeechRecognition/)  
- [pyttsx3](https://pypi.org/project/pyttsx3/)  
- [wikipedia](https://pypi.org/project/wikipedia/)  
- [requests](https://pypi.org/project/requests/)  
- [translate](https://pypi.org/project/translate/)  
- JSON  
- OpenWeatherMap API (para informações climáticas)

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

```bash
pip install SpeechRecognition pyttsx3 wikipedia requests translate
```

Além disso, é necessário:
- Um microfone conectado ao seu computador.
- A chave da API da OpenWeatherMap (já configurada no código).

## Como usar

1. Execute o programa:
    ```bash
    python jarvis.py
    ```
2. Aguarde o Jarvis inicializar e diga **"Ei Jarvis"** ou uma variação como "hey jar", "ei jair", etc.
3. Dê comandos como:
   - "Que horas são"
   - "Clima em São Paulo"
   - "Criar lembrete"
   - "Ver lembrete"
   - "Procurar por inteligência artificial"
4. Para encerrar uma conversa, diga "sair" ou "muito obrigado".

## Organização do Código

O projeto é dividido em:
- **Configurações iniciais** (voz, API, variáveis)
- **Funções utilitárias** (falar, ouvir, buscar hora, clima, tocar música, piadas, tradução)
- **Funções de lembrete** (criação e consulta com persistência em JSON)
- **Função principal** (detecção de ativação por voz e execução dos comandos)
- **Detecção flexível do comando "Ei Jarvis"** (com variações semelhantes)

## Autor

Desenvolvido por **Eduardo Machado Ferla**

