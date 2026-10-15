"""
Sistema de Gestão de Perdas na Colheita de Cana-de-Açúcar
Programa integrado: menus e estruturas (Integrante 1), funções e validações (Integrante 2),
arquivos TXT/JSON (Integrante 3) e persistência Oracle (Integrante 4).

Os registros ficam em memória durante a execução. O usuário escolhe no menu quando salvar
em JSON, carregar do JSON, gerar o relatório TXT ou enviar os dados ao Oracle.
"""

from datetime import datetime
import json
import os
from math import isfinite
from typing import Dict, List, Optional, Tuple


# Tuplas: opções fixas que não precisam ser alteradas durante a execução.
TIPOS_COLHEITA: Tuple[str, ...] = ("Manual", "Mecanizada")
OPCOES_MENU: Tuple[str, ...] = (
    "1 - Cadastrar talhão",
    "2 - Registrar colheita",
    "3 - Listar talhões",
    "4 - Listar colheitas",
    "5 - Consultar colheitas por talhão",
    "6 - Salvar dados em arquivo JSON",
    "7 - Carregar dados do arquivo JSON",
    "8 - Gerar relatório de perdas (TXT)",
    "9 - Ler relatório de perdas (TXT)",
    "10 - Salvar dados no Oracle",
    "0 - Sair",
)

# Listas de dicionários: cada item contém os dados de um cadastro.
talhoes: List[Dict[str, object]] = []
colheitas: List[Dict[str, object]] = []


def proximo_id(registros: List[Dict[str, object]]) -> int:
    """Retorna o próximo identificador da lista informada."""
    if not registros:
        return 1
    return max(int(registro["id"]) for registro in registros) + 1


def ler_texto(mensagem: str) -> str:
    """Lê um texto obrigatório e impede que seja enviado vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("O campo não pode ficar vazio.")


def ler_numero(
    mensagem: str,
    minimo: float = 0,
    maximo: Optional[float] = None,
) -> float:
    """Lê um número, aceitando vírgula ou ponto como separador decimal."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if not isfinite(valor):
                raise ValueError

            if valor < minimo:
                print(f"Informe um valor igual ou maior que {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Informe um valor igual ou menor que {maximo}.")
                continue

            return valor
        except ValueError:
            print("Entrada inválida. Digite um número, por exemplo: 12,5.")


def ler_data() -> str:
    """Lê uma data em DD/MM/AAAA e a guarda no formato ISO AAAA-MM-DD."""
    while True:
        entrada = input("Data da colheita (DD/MM/AAAA): ").strip()
        try:
            data = datetime.strptime(entrada, "%d/%m/%Y")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA.")


def exibir_data(data_iso: str) -> str:
    """Converte a data armazenada para o formato usado na tela."""
    return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")


def escolher_tipo_colheita() -> str:
    """Apresenta as opções imutáveis de tipo de colheita."""
    print("\nTipo de colheita:")
    for numero, tipo in enumerate(TIPOS_COLHEITA, start=1):
        print(f"{numero} - {tipo}")

    while True:
        escolha = input("Escolha uma opção: ").strip()
        if escolha.isdigit():
            indice = int(escolha) - 1
            if 0 <= indice < len(TIPOS_COLHEITA):
                return TIPOS_COLHEITA[indice]
        print("Opção inválida. Escolha um dos tipos exibidos.")


def cadastrar_talhao() -> None:
    """Cadastra um talhão e o adiciona à lista em memória."""
    print("\n--- Cadastro de talhão ---")
    nome = ler_texto("Nome ou identificação do talhão: ")
    area_ha = ler_numero("Área do talhão em hectares: ", minimo=0.000001)

    talhao: Dict[str, object] = {
        "id": proximo_id(talhoes),
        "nome": nome,
        "area_ha": area_ha,
    }
    talhoes.append(talhao)
    print(f"Talhão cadastrado com o ID {talhao['id']}.")


def registrar_colheita() -> None:
    """Registra uma colheita vinculada a um talhão já cadastrado."""
    if not talhoes:
        print("\nCadastre um talhão antes de registrar uma colheita.")
        return

    print("\n--- Talhões disponíveis ---")
    listar_talhoes()

    while True:
        entrada_id = input("ID do talhão da colheita: ").strip()
        if entrada_id.isdigit():
            talhao_id = int(entrada_id)
            if any(int(talhao["id"]) == talhao_id for talhao in talhoes):
                break
        print("ID não encontrado. Escolha um dos talhões cadastrados.")

    print("\n--- Dados da colheita ---")
    data = ler_data()
    tipo = escolher_tipo_colheita()
    producao_t = ler_numero("Produção considerada (toneladas): ", minimo=0)
    perda_percentual = ler_numero(
        "Percentual de perda estimado (0 a 100): ",
        minimo=0,
        maximo=100,
    )
    preco_tonelada = ler_numero(
        "Preço considerado por tonelada em R$: ",
        minimo=0,
    )

    colheita: Dict[str, object] = {
        "id": proximo_id(colheitas),
        "talhao_id": talhao_id,
        "data": data,
        "tipo_colheita": tipo,
        "producao_t": producao_t,
        "perda_percentual": perda_percentual,
        "preco_tonelada": preco_tonelada,
    }
    colheitas.append(colheita)
    print(f"Colheita registrada com o ID {colheita['id']}.")


def buscar_talhao(talhao_id: int) -> Optional[Dict[str, object]]:
    """Localiza um talhão pelo ID ou retorna None."""
    for talhao in talhoes:
        if int(talhao["id"]) == talhao_id:
            return talhao
    return None


def listar_talhoes() -> None:
    """Exibe todos os talhões cadastrados."""
    print("\n--- Talhões cadastrados ---")
    if not talhoes:
        print("Nenhum talhão cadastrado.")
        return

    for talhao in talhoes:
        print(
            f"ID: {talhao['id']} | "
            f"Talhão: {talhao['nome']} | "
            f"Área: {float(talhao['area_ha']):.2f} ha"
        )



# ============================================================
# PARTE DO INTEGRANTE 2 — FUNÇÕES DE CÁLCULO E VALIDAÇÃO
# ============================================================

def calcular_perdas(
    producao_t: float,
    perda_percentual: float,
    preco_tonelada: float,
) -> Dict[str, float]:
    """
    Calcula toneladas perdidas e prejuízo estimado.

    Parâmetros:
        producao_t: produção total considerada, em toneladas.
        perda_percentual: percentual de perda informado (0 a 100).
        preco_tonelada: preço considerado por tonelada, em reais.

    Retorna um dicionário com os resultados calculados.
    """
    valores = (producao_t, perda_percentual, preco_tonelada)
    if not all(isfinite(float(valor)) for valor in valores):
        raise ValueError("Os valores precisam ser números finitos.")
    if producao_t < 0:
        raise ValueError("A produção não pode ser negativa.")
    if not 0 <= perda_percentual <= 100:
        raise ValueError("O percentual de perda deve estar entre 0 e 100.")
    if preco_tonelada < 0:
        raise ValueError("O preço por tonelada não pode ser negativo.")

    toneladas_perdidas = producao_t * (perda_percentual / 100)
    producao_aproveitada = producao_t - toneladas_perdidas
    prejuizo_estimado = toneladas_perdidas * preco_tonelada
    valor_bruto_estimado = producao_t * preco_tonelada
    valor_aproveitado_estimado = producao_aproveitada * preco_tonelada

    return {
        "toneladas_perdidas": toneladas_perdidas,
        "producao_aproveitada": producao_aproveitada,
        "prejuizo_estimado": prejuizo_estimado,
        "valor_bruto_estimado": valor_bruto_estimado,
        "valor_aproveitado_estimado": valor_aproveitado_estimado,
    }


def calcular_perda_referencia(
    tipo_colheita: str,
    producao_t: float,
    preco_tonelada: float,
) -> Dict[str, float]:
    """
    Estima perdas de referência mencionadas no guia do projeto:
    5% para colheita manual e 15% para colheita mecanizada.
    Esses percentuais são referências didáticas do trabalho.
    """
    taxas_referencia = {
        "Manual": 5.0,
        "Mecanizada": 15.0,
    }
    if tipo_colheita not in taxas_referencia:
        raise ValueError("Tipo de colheita inválido.")
    return calcular_perdas(
        producao_t,
        taxas_referencia[tipo_colheita],
        preco_tonelada,
    )


def calcular_e_exibir_resultados(colheita: Dict[str, object]) -> None:
    """Calcula e apresenta a perda informada e a referência do tipo de colheita."""
    try:
        producao_t = float(colheita["producao_t"])
        perda_percentual = float(colheita["perda_percentual"])
        preco_tonelada = float(colheita["preco_tonelada"])
        tipo = str(colheita["tipo_colheita"])

        resultado = calcular_perdas(
            producao_t,
            perda_percentual,
            preco_tonelada,
        )
        referencia = calcular_perda_referencia(
            tipo,
            producao_t,
            preco_tonelada,
        )

        print("  -- Cálculo da perda informada --")
        print(f"  Toneladas perdidas: {resultado['toneladas_perdidas']:.2f} t")
        print(f"  Produção aproveitada: {resultado['producao_aproveitada']:.2f} t")
        print(f"  Prejuízo estimado: R$ {resultado['prejuizo_estimado']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        print(f"  Valor bruto estimado: R$ {resultado['valor_bruto_estimado']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        taxa_referencia = 5.0 if tipo == "Manual" else 15.0
        print(f"  Referência didática para colheita {tipo.lower()}: {taxa_referencia:.0f}%")
        print(f"  Prejuízo estimado pela referência: R$ {referencia['prejuizo_estimado']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    except (KeyError, TypeError, ValueError) as erro:
        print(f"Não foi possível calcular os resultados: {erro}")


def exibir_colheita(colheita: Dict[str, object]) -> None:
    """Exibe uma colheita e os dados do talhão associado."""
    talhao = buscar_talhao(int(colheita["talhao_id"]))
    nome_talhao = str(talhao["nome"]) if talhao else "Talhão não localizado"

    print(
        f"ID: {colheita['id']} | "
        f"Talhão: {nome_talhao} (ID {colheita['talhao_id']}) | "
        f"Data: {exibir_data(str(colheita['data']))} | "
        f"Tipo: {colheita['tipo_colheita']} | "
        f"Produção: {float(colheita['producao_t']):.2f} t | "
        f"Perda estimada: {float(colheita['perda_percentual']):.2f}% | "
        f"Preço considerado: R$ {float(colheita['preco_tonelada']):.2f}/t"
    )
    calcular_e_exibir_resultados(colheita)


def listar_colheitas(registros: Optional[List[Dict[str, object]]] = None) -> None:
    """Exibe as colheitas; permite receber uma lista filtrada."""
    lista = colheitas if registros is None else registros
    print("\n--- Colheitas registradas ---")
    if not lista:
        print("Nenhuma colheita registrada.")
        return

    for colheita in lista:
        exibir_colheita(colheita)


def consultar_colheitas_por_talhao() -> None:
    """Filtra as colheitas pelo identificador do talhão."""
    if not talhoes:
        print("\nNenhum talhão cadastrado.")
        return

    listar_talhoes()
    entrada_id = input("\nInforme o ID do talhão: ").strip()
    if not entrada_id.isdigit():
        print("ID inválido.")
        return

    talhao_id = int(entrada_id)
    talhao = buscar_talhao(talhao_id)
    if talhao is None:
        print("Talhão não encontrado.")
        return

    registros = [
        colheita
        for colheita in colheitas
        if int(colheita["talhao_id"]) == talhao_id
    ]
    print(f"\nColheitas do talhão {talhao['nome']}:")
    listar_colheitas(registros)



# ============================================================
# PARTE DO INTEGRANTE 4 — CONEXÃO E PERSISTÊNCIA NO ORACLE
# ============================================================

def conectar_oracle():
    """
    Abre a conexão usando variáveis de ambiente:
    ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN.
    Exemplo de DSN: localhost:1521/FREEPDB1
    """
    try:
        import oracledb
    except ImportError as erro:
        raise RuntimeError(
            "Biblioteca oracledb não instalada. Execute: pip install oracledb"
        ) from erro

    usuario = os.getenv("ORACLE_USER")
    senha = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")

    if not usuario or not senha or not dsn:
        raise RuntimeError(
            "Configure ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN "
            "nas variáveis de ambiente antes de salvar no Oracle."
        )

    return oracledb.connect(user=usuario, password=senha, dsn=dsn)


def criar_tabelas_oracle(conexao) -> None:
    """Cria as tabelas do projeto se ainda não existirem."""
    comandos = [
        """
        CREATE TABLE AGRO_TALHOES (
            ID NUMBER(10) PRIMARY KEY,
            NOME VARCHAR2(200) NOT NULL,
            AREA_HA NUMBER(12,4) NOT NULL
        )
        """,
        """
        CREATE TABLE AGRO_COLHEITAS (
            ID NUMBER(10) PRIMARY KEY,
            TALHAO_ID NUMBER(10) NOT NULL,
            DATA_COLHEITA DATE NOT NULL,
            TIPO_COLHEITA VARCHAR2(20) NOT NULL,
            PRODUCAO_T NUMBER(14,3) NOT NULL,
            PERDA_PERCENTUAL NUMBER(5,2) NOT NULL,
            PRECO_TONELADA NUMBER(14,2) NOT NULL,
            CONSTRAINT FK_AGRO_COL_TALHAO
                FOREIGN KEY (TALHAO_ID) REFERENCES AGRO_TALHOES(ID)
        )
        """
    ]

    with conexao.cursor() as cursor:
        for comando in comandos:
            try:
                cursor.execute(comando)
            except Exception as erro:
                # ORA-00955: nome já utilizado por objeto existente.
                # A exceção é ignorada somente quando a tabela já existe.
                codigo = getattr(getattr(erro, "args", [None])[0], "code", None)
                mensagem = str(erro)
                if codigo == 955 or "ORA-00955" in mensagem:
                    continue
                raise


def salvar_talhoes_oracle(conexao, registros: List[Dict[str, object]]) -> int:
    """Insere ou atualiza talhões pelo ID (operação idempotente)."""
    if not registros:
        return 0

    sql = """
        MERGE INTO AGRO_TALHOES destino
        USING (
            SELECT :id AS id, :nome AS nome, :area_ha AS area_ha
            FROM dual
        ) origem
        ON (destino.ID = origem.id)
        WHEN MATCHED THEN UPDATE SET
            destino.NOME = origem.nome,
            destino.AREA_HA = origem.area_ha
        WHEN NOT MATCHED THEN INSERT (ID, NOME, AREA_HA)
            VALUES (origem.id, origem.nome, origem.area_ha)
    """
    dados = [
        {
            "id": int(item["id"]),
            "nome": str(item["nome"]),
            "area_ha": float(item["area_ha"]),
        }
        for item in registros
    ]
    with conexao.cursor() as cursor:
        cursor.executemany(sql, dados)
    return len(dados)


def salvar_colheitas_oracle(conexao, registros: List[Dict[str, object]]) -> int:
    """Insere ou atualiza colheitas pelo ID e mantém o vínculo com o talhão."""
    if not registros:
        return 0

    sql = """
        MERGE INTO AGRO_COLHEITAS destino
        USING (
            SELECT :id AS id,
                   :talhao_id AS talhao_id,
                   :data_colheita AS data_colheita,
                   :tipo_colheita AS tipo_colheita,
                   :producao_t AS producao_t,
                   :perda_percentual AS perda_percentual,
                   :preco_tonelada AS preco_tonelada
            FROM dual
        ) origem
        ON (destino.ID = origem.id)
        WHEN MATCHED THEN UPDATE SET
            destino.TALHAO_ID = origem.talhao_id,
            destino.DATA_COLHEITA = origem.data_colheita,
            destino.TIPO_COLHEITA = origem.tipo_colheita,
            destino.PRODUCAO_T = origem.producao_t,
            destino.PERDA_PERCENTUAL = origem.perda_percentual,
            destino.PRECO_TONELADA = origem.preco_tonelada
        WHEN NOT MATCHED THEN INSERT (
            ID, TALHAO_ID, DATA_COLHEITA, TIPO_COLHEITA,
            PRODUCAO_T, PERDA_PERCENTUAL, PRECO_TONELADA
        ) VALUES (
            origem.id, origem.talhao_id, origem.data_colheita,
            origem.tipo_colheita, origem.producao_t,
            origem.perda_percentual, origem.preco_tonelada
        )
    """
    dados = [
        {
            "id": int(item["id"]),
            "talhao_id": int(item["talhao_id"]),
            "data_colheita": datetime.strptime(str(item["data"]), "%Y-%m-%d"),
            "tipo_colheita": str(item["tipo_colheita"]),
            "producao_t": float(item["producao_t"]),
            "perda_percentual": float(item["perda_percentual"]),
            "preco_tonelada": float(item["preco_tonelada"]),
        }
        for item in registros
    ]
    with conexao.cursor() as cursor:
        cursor.executemany(sql, dados)
    return len(dados)


def persistir_dados_oracle(
    registros_talhoes: List[Dict[str, object]],
    registros_colheitas: List[Dict[str, object]],
) -> None:
    """
    Cria as tabelas e persiste os registros atuais.
    Os talhões são gravados antes das colheitas por causa da chave estrangeira.
    """
    conexao = None
    try:
        conexao = conectar_oracle()
        criar_tabelas_oracle(conexao)
        quantidade_talhoes = salvar_talhoes_oracle(conexao, registros_talhoes)
        quantidade_colheitas = salvar_colheitas_oracle(conexao, registros_colheitas)
        conexao.commit()
        print("\nDados persistidos no Oracle com sucesso.")
        print(f"Talhões enviados: {quantidade_talhoes}")
        print(f"Colheitas enviadas: {quantidade_colheitas}")
    except Exception as erro:
        if conexao is not None:
            conexao.rollback()
        print(f"\nNão foi possível salvar os dados no Oracle: {erro}")
        print("Verifique as credenciais, o DSN, a rede e as permissões do usuário Oracle.")
    finally:
        if conexao is not None:
            conexao.close()


# ============================================================
# PARTE DO INTEGRANTE 3 — ARQUIVOS TXT E JSON
# ============================================================

ARQUIVO_JSON = "dados_agro.json"
ARQUIVO_TXT = "relatorio_perdas.txt"


def formatar_moeda(valor: float) -> str:
    """Formata um número como moeda brasileira, por exemplo: R$ 1.234,50."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def validar_dados_carregados(dados: object) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """
    Confere se o conteúdo lido do JSON tem a estrutura esperada.
    Retorna (talhoes, colheitas) já convertidos; levanta ValueError se algo estiver errado.
    """
    if not isinstance(dados, dict):
        raise ValueError("o arquivo deve conter um objeto com as chaves 'talhoes' e 'colheitas'.")
    if not isinstance(dados.get("talhoes"), list) or not isinstance(dados.get("colheitas"), list):
        raise ValueError("as chaves 'talhoes' e 'colheitas' precisam existir e ser listas.")

    talhoes_lidos: List[Dict[str, object]] = []
    for item in dados["talhoes"]:
        try:
            talhao = {
                "id": int(item["id"]),
                "nome": str(item["nome"]).strip(),
                "area_ha": float(item["area_ha"]),
            }
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"talhão inválido ou incompleto: {item}")
        if not talhao["nome"] or not isfinite(talhao["area_ha"]) or talhao["area_ha"] <= 0:
            raise ValueError(f"talhão com nome vazio ou área inválida: {item}")
        talhoes_lidos.append(talhao)

    ids_talhoes = [t["id"] for t in talhoes_lidos]
    if len(ids_talhoes) != len(set(ids_talhoes)):
        raise ValueError("há talhões com ID repetido.")

    colheitas_lidas: List[Dict[str, object]] = []
    for item in dados["colheitas"]:
        try:
            colheita = {
                "id": int(item["id"]),
                "talhao_id": int(item["talhao_id"]),
                "data": str(item["data"]),
                "tipo_colheita": str(item["tipo_colheita"]),
                "producao_t": float(item["producao_t"]),
                "perda_percentual": float(item["perda_percentual"]),
                "preco_tonelada": float(item["preco_tonelada"]),
            }
            datetime.strptime(colheita["data"], "%Y-%m-%d")
            calcular_perdas(
                colheita["producao_t"],
                colheita["perda_percentual"],
                colheita["preco_tonelada"],
            )
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"colheita inválida ou incompleta: {item}")
        if colheita["tipo_colheita"] not in TIPOS_COLHEITA:
            raise ValueError(f"tipo de colheita desconhecido: {colheita['tipo_colheita']}")
        if colheita["talhao_id"] not in ids_talhoes:
            raise ValueError(f"colheita {colheita['id']} aponta para um talhão que não existe.")
        colheitas_lidas.append(colheita)

    ids_colheitas = [c["id"] for c in colheitas_lidas]
    if len(ids_colheitas) != len(set(ids_colheitas)):
        raise ValueError("há colheitas com ID repetido.")

    return talhoes_lidos, colheitas_lidas


def salvar_json(
    registros_talhoes: List[Dict[str, object]],
    registros_colheitas: List[Dict[str, object]],
    caminho: str = ARQUIVO_JSON,
) -> bool:
    """Grava talhões e colheitas em um único arquivo JSON. Retorna True se deu certo."""
    dados = {"talhoes": registros_talhoes, "colheitas": registros_colheitas}
    temporario = caminho + ".tmp"
    try:
        # Grava primeiro em um arquivo temporário para não corromper o arquivo anterior.
        with open(temporario, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        os.replace(temporario, caminho)
        return True
    except (OSError, TypeError) as erro:
        print(f"Não foi possível salvar o arquivo JSON: {erro}")
        return False


def carregar_json(
    caminho: str = ARQUIVO_JSON,
) -> Optional[Tuple[List[Dict[str, object]], List[Dict[str, object]]]]:
    """
    Lê o arquivo JSON e devolve (talhoes, colheitas).
    Se o arquivo não existir, estiver corrompido ou inválido, mostra o motivo e devolve None.
    """
    if not os.path.exists(caminho):
        print(f"Arquivo '{caminho}' não encontrado. Salve os dados antes de carregar.")
        return None
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return validar_dados_carregados(dados)
    except json.JSONDecodeError as erro:
        print(f"O arquivo '{caminho}' está corrompido ou não é um JSON válido ({erro}).")
    except ValueError as erro:
        print(f"O arquivo '{caminho}' tem conteúdo inválido: {erro}")
    except OSError as erro:
        print(f"Não foi possível abrir o arquivo '{caminho}': {erro}")
    return None


def montar_relatorio(
    registros_talhoes: List[Dict[str, object]],
    registros_colheitas: List[Dict[str, object]],
) -> List[str]:
    """Monta as linhas do relatório de perdas, com detalhes e totais."""
    linhas: List[str] = []
    linhas.append("RELATÓRIO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR")
    linhas.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("=" * 60)

    total_producao = total_perdida = total_prejuizo = 0.0
    totais_por_tipo: Dict[str, Dict[str, float]] = {
        tipo: {"producao": 0.0, "perdida": 0.0, "prejuizo": 0.0} for tipo in TIPOS_COLHEITA
    }

    for talhao in registros_talhoes:
        linhas.append("")
        linhas.append(
            f"TALHÃO {talhao['id']} - {talhao['nome']} ({float(talhao['area_ha']):.2f} ha)"
        )
        linhas.append("-" * 60)
        do_talhao = [c for c in registros_colheitas if int(c["talhao_id"]) == int(talhao["id"])]
        if not do_talhao:
            linhas.append("Nenhuma colheita registrada.")
            continue

        producao_talhao = perdida_talhao = prejuizo_talhao = 0.0
        for colheita in do_talhao:
            resultado = calcular_perdas(
                float(colheita["producao_t"]),
                float(colheita["perda_percentual"]),
                float(colheita["preco_tonelada"]),
            )
            linhas.append(
                f"Colheita {colheita['id']} | {exibir_data(str(colheita['data']))} | "
                f"{colheita['tipo_colheita']}"
            )
            linhas.append(
                f"  Produção: {float(colheita['producao_t']):.2f} t | "
                f"Perda: {float(colheita['perda_percentual']):.2f}% "
                f"({resultado['toneladas_perdidas']:.2f} t)"
            )
            linhas.append(
                f"  Preço: {formatar_moeda(float(colheita['preco_tonelada']))}/t | "
                f"Prejuízo estimado: {formatar_moeda(resultado['prejuizo_estimado'])}"
            )
            producao_talhao += float(colheita["producao_t"])
            perdida_talhao += resultado["toneladas_perdidas"]
            prejuizo_talhao += resultado["prejuizo_estimado"]

            tipo = str(colheita["tipo_colheita"])
            totais_por_tipo[tipo]["producao"] += float(colheita["producao_t"])
            totais_por_tipo[tipo]["perdida"] += resultado["toneladas_perdidas"]
            totais_por_tipo[tipo]["prejuizo"] += resultado["prejuizo_estimado"]

        linhas.append(
            f"Total do talhão: produção {producao_talhao:.2f} t | "
            f"perdas {perdida_talhao:.2f} t | prejuízo {formatar_moeda(prejuizo_talhao)}"
        )
        total_producao += producao_talhao
        total_perdida += perdida_talhao
        total_prejuizo += prejuizo_talhao

    linhas.append("")
    linhas.append("=" * 60)
    linhas.append("TOTAIS POR TIPO DE COLHEITA")
    for tipo, totais in totais_por_tipo.items():
        linhas.append(
            f"  {tipo}: produção {totais['producao']:.2f} t | "
            f"perdas {totais['perdida']:.2f} t | prejuízo {formatar_moeda(totais['prejuizo'])}"
        )
    linhas.append("")
    linhas.append("TOTAL GERAL")
    linhas.append(
        f"  Produção {total_producao:.2f} t | perdas {total_perdida:.2f} t | "
        f"prejuízo {formatar_moeda(total_prejuizo)}"
    )
    return linhas


def exportar_relatorio_txt(
    registros_talhoes: List[Dict[str, object]],
    registros_colheitas: List[Dict[str, object]],
    caminho: str = ARQUIVO_TXT,
) -> bool:
    """Gera o relatório de perdas em arquivo TXT. Retorna True se deu certo."""
    try:
        linhas = montar_relatorio(registros_talhoes, registros_colheitas)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas) + "\n")
        return True
    except (OSError, KeyError, TypeError, ValueError) as erro:
        print(f"Não foi possível gerar o relatório TXT: {erro}")
        return False


def ler_relatorio_txt(caminho: str = ARQUIVO_TXT) -> bool:
    """Lê o relatório TXT e o exibe na tela. Retorna True se conseguiu ler."""
    if not os.path.exists(caminho):
        print(f"Relatório '{caminho}' não encontrado. Gere o relatório antes de lê-lo.")
        return False
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except OSError as erro:
        print(f"Não foi possível ler o relatório: {erro}")
        return False
    print()
    print(conteudo)
    return True


def menu_salvar_json() -> None:
    """Opção do menu: salva os dados atuais em JSON."""
    if not talhoes and not colheitas:
        print("\nNão há dados para salvar.")
        return
    if salvar_json(talhoes, colheitas):
        print(f"\nDados salvos em '{ARQUIVO_JSON}' "
              f"({len(talhoes)} talhão(ões) e {len(colheitas)} colheita(s)).")


def menu_carregar_json() -> None:
    """Opção do menu: carrega os dados do JSON, substituindo os que estão em memória."""
    if talhoes or colheitas:
        resposta = input("Os dados atuais em memória serão substituídos. Continuar? (s/n): ").strip().lower()
        if resposta != "s":
            print("Carregamento cancelado.")
            return
    resultado = carregar_json()
    if resultado is None:
        print("Os dados em memória foram mantidos.")
        return
    # Atribuição por fatias mantém as mesmas listas usadas pelo restante do programa.
    talhoes[:] = resultado[0]
    colheitas[:] = resultado[1]
    print(f"\nDados carregados: {len(talhoes)} talhão(ões) e {len(colheitas)} colheita(s).")


def menu_gerar_relatorio() -> None:
    """Opção do menu: gera o relatório TXT."""
    if not colheitas:
        print("\nRegistre ao menos uma colheita para gerar o relatório.")
        return
    if exportar_relatorio_txt(talhoes, colheitas):
        print(f"\nRelatório gerado em '{ARQUIVO_TXT}'.")


def exibir_menu() -> None:
    """Mostra as opções principais do sistema."""
    print("\n=== Sistema de Gestão de Perdas na Colheita de Cana ===")
    for opcao in OPCOES_MENU:
        print(opcao)


def executar_menu() -> None:
    """Mantém o sistema em execução até o usuário escolher sair."""
    while True:
        exibir_menu()
        opcao = input("Selecione uma opção: ").strip()

        if opcao == "1":
            cadastrar_talhao()
        elif opcao == "2":
            registrar_colheita()
        elif opcao == "3":
            listar_talhoes()
        elif opcao == "4":
            listar_colheitas()
        elif opcao == "5":
            consultar_colheitas_por_talhao()
        elif opcao == "6":
            menu_salvar_json()
        elif opcao == "7":
            menu_carregar_json()
        elif opcao == "8":
            menu_gerar_relatorio()
        elif opcao == "9":
            ler_relatorio_txt()
        elif opcao == "10":
            persistir_dados_oracle(talhoes, colheitas)
        elif opcao == "0":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida. Escolha uma opção exibida no menu.")


if __name__ == "__main__":
    try:
        executar_menu()
    except (EOFError, KeyboardInterrupt):
        print("\nExecução encerrada.")
