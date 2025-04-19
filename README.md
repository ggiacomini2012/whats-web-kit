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

Você pode criar um executável standalone (um aplicativo `.app` no macOS ou `.exe` no Windows) para que o bot possa ser executado sem precisar instalar Python ou dependências manualmente em outra máquina.

**Pré-requisitos para Build:**

*   Ter seguido os passos de **Instalação**, incluindo a instalação do `pyinstaller`.
*   Para o ícone do aplicativo no **macOS**: Você precisará converter o arquivo `icon.png` para o formato `.icns` (Apple Icon Image). Você pode usar conversores online (procure por "png to icns converter mac") ou ferramentas como `iconutil` do macOS. Salve o arquivo resultante como `icon.icns` na raiz do projeto.
*   Para o ícone do aplicativo no **Windows**: Você precisará de um arquivo `.ico`. Se não tiver um, pode converter `icon.png` para `.ico` usando conversores online.

**Comandos de Build:**

Execute o comando apropriado para seu sistema operacional no terminal, a partir da pasta raiz do projeto (com o ambiente virtual ativado):

**macOS:**

```bash
pyinstaller --windowed --name gui --icon="icon.icns" --add-data="icon.png:." --noconfirm gui.py
```

*   `--windowed`: Roda o aplicativo sem uma janela de terminal visível.
*   `--name gui`: Define o nome do aplicativo resultante (`gui.app`).
*   `--icon="icon.icns"`: Define o ícone que aparecerá no Finder para `gui.app`. **Requer o arquivo `icon.icns`**.
*   `--add-data="icon.png:."`: Inclui o arquivo `icon.png` dentro do bundle. Isso é necessário para que o código possa carregar a imagem para o ícone da *janela* do aplicativo em tempo de execução.
*   `--noconfirm`: Pula as confirmações de sobrescrever pastas `dist` e `build`.
*   `gui.py`: O script principal da aplicação.

O aplicativo (`gui.app`) será gerado na pasta `dist/`.

**Windows:**

```bash
pyinstaller --windowed --name gui --icon="icon.ico" --add-data="icon.png;." --noconfirm gui.py
```

*   `--windowed`: Roda o aplicativo sem uma janela de terminal visível.
*   `--name gui`: Define o nome do executável resultante (`gui.exe`).
*   `--icon="icon.ico"`: Define o ícone do arquivo `.exe`. **Requer um arquivo `icon.ico`**.
*   `--add-data="icon.png;."`: Inclui o arquivo `icon.png` junto ao executável. O separador `:` (macOS/Linux) é trocado por `;` no Windows.
*   `--noconfirm`: Pula as confirmações.
*   `gui.py`: O script principal da aplicação.

O executável (`gui.exe`) e seus arquivos de suporte serão gerados na pasta `dist/gui/`.

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