# Análise de Feedback com Inteligência Artificial

Aplicação web completa para análise de sentimentos e categorização de feedbacks de clientes em tempo real. O sistema combina um backend em Python com um dashboard dinâmico no frontend para exibir métricas consolidadas instantaneamente.

## Funcionalidades

* **Análise em Tempo Real:** Processamento imediato de feedbacks através de requisições assíncronas, sem necessidade de recarregar a página.
* **Resiliência de API:** Sistema de contingência dinâmica que seleciona automaticamente os modelos mais estáveis e disponíveis do momento via OpenRouter.
* **Dashboard Dinâmico:** Gráfico de rosca interativo que atualiza suas fatias proporcionalmente a cada nova análise computada.
* **Notificações Fluidas:** Alertas visuais de status (carregamento, sucesso e erro) integrados à interface do usuário.
* **Histórico Visual:** Exibição dos resultados anteriores estruturados em cards coloridos de acordo com o sentimento detectado.

## Tecnologias

* **Backend:** Python 3.14, Flask, Python-dotenv
* **Inteligência Artificial:** OpenRouter API (LLM dinâmico)
* **Frontend:** JavaScript (Fetch API), Chart.js, Toastify-JS, HTML5, CSS3
* **Deploy & Infraestrutura:** Vercel (Serverless), GitHub (CI/CD)

## Estrutura do Projeto

```text
analise-feedback/
├── templates/
│   └── index.html       # Interface do usuário e dashboard
├── app.py               # Servidor Flask e lógica de integração com IA
├── requirements.txt     # Dependências mínimas do projeto
├── vercel.json          # Configuração de deploy da Vercel
├── .env                 # Chave de API local (não versionada)
└── .gitignore           # Proteção de arquivos sensíveis
