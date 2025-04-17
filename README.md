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

Para gerar o executável diretamente usando PyInstaller (certifique-se de ter as dependências instaladas e estar no ambiente virtual), você pode usar o seguinte comando no terminal a partir da raiz do projeto:

```bash
pyinstaller --windowed --icon="icon2.ico" --add-data="icon2.png;." --clean --add-data="bot.py;." gui.py
```

*   `--windowed`: Esconde a janela do terminal ao executar o app.
*   `--icon="icon2.ico"`: Define o ícone do arquivo `.exe`.
*   `--add-data="<arquivo>;."`: Inclui arquivos adicionais (como imagens ou outros scripts) necessários para a aplicação.
*   `--clean`: Limpa o cache e arquivos de build anteriores antes de começar.
*   `gui.py`: O script principal da sua aplicação.

O executável será gerado na pasta `dist/gui`.

## Limpeza / Desinstalação

Para remover os arquivos e pastas gerados pelo processo de build e pela execução do bot (como `dist`, `build`, `bot.log`, `contact_log.json` e o ambiente virtual `.venv`), você pode usar os scripts de limpeza fornecidos. **Atenção:** Estes scripts NÃO apagam os arquivos de código fonte (`gui.py`, `bot.py`, etc.).

*   **Windows:**
    Execute o arquivo `uninstall.bat` com um duplo clique. Ele pedirá confirmação antes de remover os arquivos.

*   **macOS / Linux:**
    Execute o arquivo `uninstall.sh` a partir do seu terminal. Pode ser necessário dar permissão de execução ao script primeiro:
    ```bash
    chmod +x uninstall.sh
    ```
    Depois, execute-o:
    ```bash
    ./uninstall.sh
    ```
    O script também pedirá confirmação.

## Estrutura do Projeto

```