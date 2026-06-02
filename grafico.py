import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("resultado_feedback.csv")

cores = {"Positivo": "#4CAF50", "Negativo": "#F44336", "Neutro": "#FF9800"}
contagem = df["sentimento"].value_counts()
labels = contagem.index.tolist()
valores = contagem.values.tolist()
colors = [cores.get(l, "#9E9E9E") for l in labels]

fig, ax = plt.subplots(figsize=(6, 6))
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
print("Gráfico salvo!")
plt.show()