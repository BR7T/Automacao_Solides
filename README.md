# 🚀 Automação Sólides

Este projeto tem como objetivo automatizar processos relacionados à plataforma **Sólides**, utilizando **Python** e **PyInstaller** para geração de um executável independente que adiciona informações da plataforma ao seu banco **MSSQL**.

---

## 🧩 Tecnologias Utilizadas

- **Python 3.12+**
- **PyInstaller**
- **dotenv** (para variáveis de ambiente)
- **Bibliotecas auxiliares** listadas em `requirements.txt`

---

## ⚙️ Configuração do Ambiente

### 1. Clonar o Repositório

`bash`
```
git clone https://github.com/BR7T/Automacao_Solides
cd Automacao_Solides
```
### 2. Criar e ativar o ambiente virtual 🐍

`bash`
```
python -m venv venv
```
- Windows:

    `bash`
  ```
  venv\Scripts\activate
  ```
- Linux
  ```
  source venv/bin/activate
  ```
### 3. Instalar dependências

`bash`
```
pip install -r requirements.txt
```
---
## 🔑 Configuração do arquivo `.env`
Crie um arquivo chamado `.env` na raiz do projeto e adicione as credenciais do seu banco e sua chave API:

`.env`
```
DB_HOST = caminho para seu banco
DB_DATABASE = Nome do seu banco de dados

APIKEY_SOLIDES = sua chave API
```
---
## 🗄️ Configuração do banco de dados
Para usar a automação sem alterar o código, execute o script abaixo no seu servidor MSSQL:  
`SQL`
```
-- Cria o banco de dados
CREATE DATABASE Solides;
GO

USE Solides;
GO

-- Tabela principal: Jornada
CREATE TABLE dbo.Jornada (
    id_jornada INT IDENTITY(1,1) PRIMARY KEY,
    dataJornada DATE NOT NULL,
    n_matricula INT NULL,
    minutosTrabalhados INT NOT NULL,
    nome VARCHAR(150) NOT NULL,
    id_tangerino INT NOT NULL,
    setor VARCHAR(100) NULL,
    CONSTRAINT UQ_Jornada UNIQUE (n_matricula, dataJornada)
);
GO

-- Tabela de registros de ponto
CREATE TABLE dbo.Pontos (
    id_ponto INT IDENTITY(1,1) PRIMARY KEY,
    id_tangerino INT NOT NULL,
    datahora_ponto DATETIME NULL,
    tipo TINYINT NULL,
    CONSTRAINT FK_Pontos_Jornada FOREIGN KEY (id_tangerino)
        REFERENCES dbo.Jornada (id_tangerino)
);
GO
```

## 🧱 Estrutura do projeto
```
src/
├── main.py                 # Ponto de entrada
├── functions/              
|   ├── connections.py      # Conexão com banco de dados
|   ├── convertMsToDate.py  # Função de conversão de data
|   ├── database.py         # Operações no banco
|   ├── Employee.py         # Classe de funcionário
|   └── __init__.py
|
└── functions/Solides/
    ├── get.py              # Funções de request para a API
    └── __init__.py
```
--- 
## ⚙️ Geração do executável  
Para criar o executável com o *`PyInstaller`*, rode o comando:  
`bash`  
```
pyinstaller --onefile .\src\main.py
```  
Após a conclusão, o executável estará disponível em:  
```
dist/
└── main.exe
```
---
## ▶️ Execução
Basta abrir a pasta e executar   
`bash`   
```
dist\main.exe
```

---
### 👨‍💻 Autor
Victor Buratini  
🗓️ 2025
