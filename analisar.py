import pandas as pd
import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_feedback(texto_feedback, tentativas=5):
    """Envia um feedback para o Gemini e retorna sentimento e palavra-chave."""
    prompt = f"""Analise o seguinte feedback de cliente e responda EXATAMENTE neste formato:
SENTIMENTO: [Positivo, Neutro ou Negativo]
PALAVRA_CHAVE: [uma palavra ou expressão curta que resume a principal dor ou elogio]
RESUMO: [uma frase curta explicando o motivo do sentimento]

Feedback: "{texto_feedback}"
"""
    for tentativa in range(tentativas):
        try:
            resposta = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return resposta.text
        except errors.ClientError as e:
            if "429" in str(e) and tentativa < tentativas - 1:
                espera = 30 * (tentativa + 1)
                print(f"  Limite atingido. Aguardando {espera}s antes de tentar novamente...")
                time.sleep(espera)
            else:
                raise

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

# Lê a planilha de feedbacks
print("Lendo feedbacks...")
df = pd.read_csv("feedbacks.csv")

sentimentos = []
palavras_chave = []
resumos = []

for index, row in df.iterrows():
    print(f"Analisando feedback {index + 1}/{len(df)}: {row['cliente']}...")
    resposta = analisar_feedback(row["feedback"])
    sentimento, palavra_chave, resumo = extrair_campos(resposta)
    sentimentos.append(sentimento)
    palavras_chave.append(palavra_chave)
    resumos.append(resumo)
    time.sleep(5)  # pausa entre requisições

df["sentimento"] = sentimentos
df["palavra_chave"] = palavras_chave
df["resumo"] = resumos

df.to_csv("resultado_feedback.csv", index=False)
print("\nArquivo 'resultado_feedback.csv' salvo com sucesso!")

print("\n===== PAINEL DE RESULTADOS =====")
print(df["sentimento"].value_counts().to_string())
print(f"\nTotal de feedbacks analisados: {len(df)}")
print("================================")

cores = {"Positivo": "#4CAF50", "Negativo": "#F44336", "Neutro": "#FF9800"}

contagem = df["sentimento"].value_counts()
labels = contagem.index.tolist()
valores = contagem.values.tolist()
colors = [cores.get(1, "#9E9E9E") for l in labels]

fig, ax = plt.subplots(figsize=(6, 6    ))
wedges, texts, autotexts = ax.pie(
    valores,
    labels=labels,
    autopct="%1.0f%%",
    colors=colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2}
)

for text in texts:
    text.set_fontsize(13)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_color("white")
    autotext.set_fontweight("bold")

ax.set_title("Análise de Sentimentos dos Feedbacks", fontsize=15, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("grafico_sentimentos.png", dpi=150, bbox_inches="tight")
print("Gráfico salvo como 'grafico_sentimentos.png'!")
plt.show()

