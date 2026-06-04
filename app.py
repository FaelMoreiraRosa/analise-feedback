from flask import Flask, request, jsonify, render_template
import time
import os
from openai import OpenAI, NotFoundError, RateLimitError
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def analisar_feedback(texto_feedback):
    prompt = f"""Analise o seguinte feedback de cliente e responda EXATAMENTE neste formato:
SENTIMENTO: [Positivo, Neutro ou Negativo]
PALAVRA_CHAVE: [uma palavra ou expressão curta que resume a principal dor ou elogio]
RESUMO: [uma frase curta explicando o motivo do sentimento]

Feedback: "{texto_feedback}"
"""
    try:
        
        resposta = client.chat.completions.create(
            model="openrouter/auto", 
            messages=[{"role": "user", "content": prompt}]
        )
        return resposta.choices[0].message.content
        
    except Exception as e:
        print(f"\n[ERRO NA API]: {e}")

        return "SENTIMENTO: Erro\nPALAVRA_CHAVE: Instabilidade\nRESUMO: O servidor de IA está temporariamente indisponível."
    
def extrair_campos(resposta):
    sentimento = "Indefinido"
    palavra_chave = "Indefinido"
    resumo = "Indefinido"

    for linha in resposta.strip().split("\n"):
        if linha.startswith("SENTIMENTO:"):
            sentimento = linha.replace("SENTIMENTO:", "").strip()
        elif linha.startswith("PALAVRA_CHAVE:"):
            palavra_chave = linha.replace("PALAVRA_CHAVE:", "").strip()
        elif linha.startswith("RESUMO:"):
            resumo = linha.replace("RESUMO:", "").strip()

    return sentimento, palavra_chave, resumo

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisar", methods=["POST"])
def analisar():
    dados = request.get_json()
    cliente = dados.get("cliente")
    feedback = dados.get("feedback")

    if not cliente or not feedback:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    resposta = analisar_feedback(feedback)
    sentimento, palavra_chave, resumo = extrair_campos(resposta)

    if sentimento == "Erro":
        return jsonify({
            "erro": "O servidor de IA está instável. Tente novamente em instantes.",
            "sentimento": "Erro",
            "resumo": resumo
        }), 502 

    return jsonify({
        "cliente": cliente,
        "feedback": feedback,
        "sentimento": sentimento,
        "palavra_chave": palavra_chave,
        "resumo": resumo
    })

if __name__ == "__main__":
    app.run(debug=True)