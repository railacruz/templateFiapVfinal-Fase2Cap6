# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Gestão de Perdas na Colheita de Cana-de-Açúcar

## Grupo - Fase 2 Cap 6 - Python e além

## 👨‍🎓 Integrantes: 
- Gabriela Pacheco (RM575120) — Integrante 1: menu e estruturas de dados
- Gabriel Pietrobon Ferreira (RM574967) — Integrante 2: funções, cálculos e validações
- Raila Santos Cruz (RM576112) — Integrante 3: arquivos TXT e JSON
- Leonardo Yokoda (RM575829) — Integrante 4: conexão e persistência no Oracle

## 👩‍🏫 Professores:
### Tutor(a) 
-  Sabrina
### Coordenador(a)
- André Godoi


## 📜 Descrição

Programa em Python, executado no terminal, para registrar talhões e colheitas de cana-de-açúcar, calcular as toneladas perdidas e o prejuízo estimado, guardar os dados em arquivos TXT e JSON e enviá-los a um banco Oracle.

A cana-de-açúcar tem grande peso na produção agrícola brasileira, mas parte do que é produzido se perde na colheita. Segundo o material da atividade, as perdas na colheita manual raramente passam de 5%, enquanto na mecanizada podem chegar a 15%. Esses percentuais são usados no programa como referência didática. Um percentual pequeno pesa muito em grandes volumes: em um talhão de 1.000 toneladas com 15% de perda, são 150 toneladas que deixam de ser aproveitadas.

O usuário cadastra talhões (nome e área em hectares) e registra colheitas ligadas a eles (data, tipo manual ou mecanizada, produção em toneladas, percentual de perda e preço por tonelada). O programa valida as entradas, calcula perdas e prejuízo, lista e consulta os registros, salva e carrega os dados em JSON, gera e lê um relatório em TXT e grava os dados no Oracle.

```
toneladas perdidas = produção × (perda % / 100)
produção aproveitada = produção − toneladas perdidas
prejuízo estimado = toneladas perdidas × preço por tonelada
```

Exemplo: 1.000 t, perda de 15% e preço de R$ 150,00/t resultam em 150 t perdidas e prejuízo de R$ 22.500,00.

Conceitos aplicados: subalgoritmos com parâmetros, listas, dicionários, tuplas, tabela de memória (listas de dicionários), arquivos TXT e JSON, banco Oracle e `try/except` na validação das entradas. O projeto é um protótipo acadêmico e não substitui sistemas profissionais do setor.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Neste projeto: `schema_oracle.sql`, com a criação das tabelas do Oracle.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto. Neste projeto: `sistema_gestao_perdas_cana.py` (programa) e `requirements.txt` (dependência do Oracle).

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.9 ou superior.
- Para as opções de menu 1 a 9 (cadastros, consultas, JSON e TXT) não é preciso instalar nada.
- Para a opção 10 (Oracle): biblioteca `oracledb` e um banco Oracle acessível.

### Executando

1. Baixe o repositório (botão **Code > Download ZIP**) e extraia a pasta.
2. No terminal, entre na pasta do projeto e execute:

```
python src/sistema_gestao_perdas_cana.py
```

### Menu

```
1 - Cadastrar talhão
2 - Registrar colheita
3 - Listar talhões
4 - Listar colheitas
5 - Consultar colheitas por talhão
6 - Salvar dados em arquivo JSON
7 - Carregar dados do arquivo JSON
8 - Gerar relatório de perdas (TXT)
9 - Ler relatório de perdas (TXT)
10 - Salvar dados no Oracle
0 - Sair
```

Os dados ficam em memória enquanto o programa está aberto. Use a opção 6 antes de sair para não perdê-los e a opção 7 para retomá-los depois.

### Arquivos TXT e JSON

Os arquivos são criados na pasta em que o programa é executado.

`dados_agro.json` guarda talhões e colheitas, com as datas no formato `AAAA-MM-DD`:

```json
{
    "talhoes": [
        {"id": 1, "nome": "Talhão Norte", "area_ha": 12.5}
    ],
    "colheitas": [
        {
            "id": 1,
            "talhao_id": 1,
            "data": "2026-05-10",
            "tipo_colheita": "Manual",
            "producao_t": 100.0,
            "perda_percentual": 5.0,
            "preco_tonelada": 150.0
        }
    ]
}
```

Ao carregar, o programa confere a estrutura: campos obrigatórios, valores numéricos, datas, tipo de colheita, IDs repetidos e colheitas ligadas a talhões inexistentes. Se o arquivo estiver ausente, corrompido ou inválido, mostra o motivo e mantém os dados que já estavam em memória.

`relatorio_perdas.txt` traz o detalhe de cada colheita por talhão, o total de cada talhão, os totais por tipo de colheita e o total geral.

### Banco de dados Oracle

A opção 10 cria as tabelas `AGRO_TALHOES` e `AGRO_COLHEITAS`, caso ainda não existam, e grava os dados em memória com `MERGE`: registros novos são inseridos e registros com o mesmo ID são atualizados. O programa só grava no banco; não lê dados de volta do Oracle.

1. Instale a biblioteca:

   ```
   pip install -r src/requirements.txt
   ```

2. Defina as variáveis de ambiente com os dados de conexão. As credenciais não ficam no código.

   Windows (PowerShell):

   ```
   $env:ORACLE_USER = "seu_usuario"
   $env:ORACLE_PASSWORD = "sua_senha"
   $env:ORACLE_DSN = "host:1521/nome_do_servico"
   ```

   Linux ou macOS:

   ```
   export ORACLE_USER="seu_usuario"
   export ORACLE_PASSWORD="sua_senha"
   export ORACLE_DSN="host:1521/nome_do_servico"
   ```

3. Execute o programa e escolha a opção 10.

O arquivo `scripts/schema_oracle.sql` traz o mesmo esquema, caso prefira criar as tabelas manualmente. Se a conexão falhar, o programa informa o erro e continua funcionando.


## 🗃 Histórico de lançamentos

* 1.0.0 - 14/10/2026
    * Versão entregue: menu, cálculos e validações, arquivos TXT e JSON e persistência no Oracle.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
