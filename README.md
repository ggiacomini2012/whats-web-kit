# whats-web-kit

Um bot para automatizar o envio de mensagens no WhatsApp Web com uma interface gráfica (GUI).

## Funcionalidades

*   Envia mensagens personalizadas para múltiplos contatos via WhatsApp Web.
*   Carrega contatos a partir de um arquivo CSV.
*   Interface gráfica (GUI) para fácil utilização.
*   Permite agendar o envio das mensagens.

## Pré-requisitos

*   **Python:** Python 3.8 ou superior ([python.org](https://www.python.org/)).
*   **Pip:** (Normalmente incluído com Python). Verifique se está no PATH.
*   **Arquivo `contacts.csv`:** Um arquivo CSV na raiz do projeto contendo os contatos. Deve ter uma coluna `phone_number` (formato internacional, ex: `+5511987654321`) e opcionalmente uma coluna `name` para personalização da mensagem com `[Name]`.
    *   Exemplo `contacts.csv`:
        ```csv
        phone_number,name
        +19998887777,Alice
        +5511987654321,Bob
        ```
*   **Arquivos de Ícone:** `icon2.png` e `icon2.ico` (necessário se for gerar o executável) na raiz do projeto.

## Instalação

1.  **Clone o Repositório (Opcional):**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd whats-web-kit
    ```
    *(Se não clonar, certifique-se de ter todos os arquivos do projeto: `gui.py`, `bot.py`, `requirements.txt`, etc.)*

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    *   Abra um terminal na pasta do projeto.
    *   Crie o ambiente:
        ```bash
        python -m venv .venv
        ```
    *   Ative o ambiente:
        *   Windows (Cmd): `.venv\Scripts\activate`
        *   Windows (PowerShell): `.venv\Scripts\Activate.ps1`
        *   macOS/Linux: `source .venv/bin/activate`

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    Dependências principais: `pywhatkit`, `customtkinter`, `pyautogui`, `pyinstaller`.

## Como Usar

Com o ambiente virtual ativado e as dependências instaladas, execute a interface gráfica:

```bash
python gui.py
```

Siga as instruções na interface para carregar o arquivo `contacts.csv`, escrever sua mensagem (use `[Name]` para personalização, se houver a coluna `name` no CSV) e agendar o envio.

## Build (Opcional)

Para instruções detalhadas sobre como gerar um executável standalone (Windows), consulte o arquivo `SETUP_GUIDE.md`.

## Estrutura do Projeto

```
/whats-web-kit
|-- gui.py             # Script principal da interface gráfica
|-- bot.py             # Lógica principal do bot (envio de mensagens)
|-- requirements.txt   # Lista de dependências Python
|-- contacts.csv       # Arquivo de contatos (precisa ser criado)
|-- icon2.png          # Ícone usado pela GUI
|-- icon2.ico          # Ícone para o executável (Windows)
|-- SETUP_GUIDE.md     # Guia detalhado de setup e build
|-- README.md          # Este arquivo
|-- .venv/             # Ambiente virtual (se criado)
|-- dist/              # Pasta de saída do build (se gerado)
|-- build/             # Pasta temporária do build (se gerado)
... (outros arquivos/pastas)
```

## Licença

(Adicione aqui informações sobre a licença, se houver)
