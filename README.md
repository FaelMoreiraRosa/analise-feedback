# Análise de Feedback com IA

Script Python que analisa feedbacks de clientes automaticamente usando a API do Google Gemini, classificando sentimento, palavra-chave e resumo de cada resposta.

## Funcionalidades

- Lê feedbacks de um arquivo CSV
- Classifica cada feedback como Positivo, Neutro ou Negativo
- Extrai palavra-chave e resumo de cada feedback
- Gera um relatório CSV com os resultados

## Tecnologias

- Python 3.14
- Google Gemini API (`google-genai`)
- Pandas

## Como usar

1. Clone o repositório
```bash
   git clone https://github.com/seu-usuario/analise-feedback.git
   cd analise-feedback
```

2. Crie e ative o ambiente virtual
```bash
   python -m venv .venv
   .venv\Scripts\activate
```

3. Instale as dependências
```bash
   pip install -r requirements.txt
```

4. Configure sua chave de API — crie um arquivo `.env`:

GEMINI_API_KEY=sua_chave_aqui

5. Adicione seus feedbacks em `feedbacks.csv` e rode:
```bash
   python analisar.py
```

## Estrutura

analise-feedback/
├── analisar.py         # Script principal
├── feedbacks.csv       # Dados de entrada
├── requirements.txt    # Dependências
├── .env                # Chave de API (não versionado)
└── .gitignore