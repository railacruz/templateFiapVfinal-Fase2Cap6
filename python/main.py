"""
FarmTech Solutions - Sistema de Gestao Agricola Digital
=========================================================

Aplicacao Python para a fazenda-cliente da FarmTech Solutions, com suporte
a 2 culturas (Cafe e Cana-de-acucar), calculo de area de plantio,
calculo de manejo de insumos e um menu interativo completo.

Premissas assumidas pelo grupo (ver README.md para detalhes):
 - Culturas suportadas: Cafe e Cana-de-acucar.
 - Cafe    -> area calculada como TRAPEZIO (talhoes em encosta / curvas de
              nivel, formato comum em cafezais de terreno inclinado).
 - Cana    -> area calculada como RETANGULO (talhao em terreno plano).
 - Manejo de insumos: o usuario informa o produto, a dose por metro linear
   de rua (em mL/metro), o numero de ruas da lavoura e o comprimento de
   cada rua (em metros). O total de insumo (em litros) e calculado como:
       total_litros = (dose_ml_por_metro * numero_de_ruas * comprimento_rua) / 1000

Os dados sao armazenados em VETORES (listas paralelas), conforme exigido
pelo enunciado: cada registro ocupa a MESMA posicao (indice) em todos os
vetores abaixo.
"""

import csv
import os

# ---------------------------------------------------------------------------
# "Banco de dados" em memoria: vetores (listas) paralelos.
# O registro de indice i e formado por vet_x[i] em todos os vetores abaixo.
# ---------------------------------------------------------------------------
vet_cultura = []            # str: "Cafe" ou "Cana-de-acucar"
vet_figura = []              # str: "Trapezio" ou "Retangulo"
vet_dim1 = []                 # float: base maior (trapezio) OU comprimento (retangulo)
vet_dim2 = []                 # float: base menor (trapezio) OU largura (retangulo)
vet_dim3 = []                 # float: altura (trapezio) OU 0.0 (retangulo, nao usado)
vet_area_m2 = []              # float: area de plantio calculada (m2)
vet_produto = []              # str: nome do insumo/produto aplicado
vet_dose_ml_m = []            # float: dose do produto em mL por metro de rua
vet_ruas = []                  # int: numero de ruas da lavoura
vet_comprimento_rua_m = []    # float: comprimento de cada rua (m)
vet_total_insumo_l = []       # float: total de insumo necessario (litros)

CULTURAS_VALIDAS = ("Cafe", "Cana-de-acucar")
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_agricolas.csv")


# ---------------------------------------------------------------------------
# Funcoes auxiliares de entrada (com loop + decisao para validar o valor)
# ---------------------------------------------------------------------------
def ler_float(mensagem):
    """Le um numero float da entrada padrao, repetindo ate ser valido (loop)."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
            if valor <= 0:
                print(">> O valor deve ser maior que zero. Tente novamente.")
                continue
            return valor
        except ValueError:
            print(">> Valor invalido. Digite um numero (ex: 12.5).")


def ler_int(mensagem):
    """Le um numero inteiro da entrada padrao, repetindo ate ser valido (loop)."""
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
            if valor <= 0:
                print(">> O valor deve ser maior que zero. Tente novamente.")
                continue
            return valor
        except ValueError:
            print(">> Valor invalido. Digite um numero inteiro (ex: 10).")


def ler_texto(mensagem):
    """Le um texto nao vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print(">> Este campo nao pode ficar vazio.")


def escolher_cultura():
    """Menu de decisao para escolher entre as 2 culturas suportadas."""
    while True:
        print("\nCulturas disponiveis:")
        print("  1 - Cafe          (area = TRAPEZIO)")
        print("  2 - Cana-de-acucar (area = RETANGULO)")
        opcao = input("Escolha a cultura (1/2): ").strip()
        if opcao == "1":
            return "Cafe"
        elif opcao == "2":
            return "Cana-de-acucar"
        else:
            print(">> Opcao invalida. Digite 1 ou 2.")


# ---------------------------------------------------------------------------
# Calculos de area (item b) e de insumos (item c)
# ---------------------------------------------------------------------------
def calcular_area(cultura, dim1, dim2, dim3):
    """
    Calcula a area de plantio de acordo com a figura geometrica da cultura.
      - Cafe -> Trapezio:   area = ((base_maior + base_menor) / 2) * altura
      - Cana -> Retangulo:  area = comprimento * largura
    Retorna (figura, area_m2).
    """
    if cultura == "Cafe":
        figura = "Trapezio"
        area = ((dim1 + dim2) / 2) * dim3
    else:  # "Cana-de-acucar"
        figura = "Retangulo"
        area = dim1 * dim2
    return figura, area


def calcular_insumo(dose_ml_m, ruas, comprimento_rua_m):
    """
    Calcula o total de insumo necessario (em litros).
    Exemplo do enunciado: pulverizar 500 mL/metro de rua com o trator.
        total_litros = (dose_ml_m * ruas * comprimento_rua_m) / 1000
    """
    total_ml = dose_ml_m * ruas * comprimento_rua_m
    return total_ml / 1000.0


# ---------------------------------------------------------------------------
# Operacoes do menu: Entrada, Saida, Atualizacao, Delecao
# ---------------------------------------------------------------------------
def cadastrar_dados():
    """Entrada de dados: cadastra um novo talhao/registro nos vetores."""
    print("\n=== ENTRADA DE DADOS (novo registro) ===")
    cultura = escolher_cultura()

    if cultura == "Cafe":
        print("\n-- Dimensoes do talhao (TRAPEZIO) --")
        dim1 = ler_float("Base maior (m): ")
        dim2 = ler_float("Base menor (m): ")
        dim3 = ler_float("Altura (m): ")
    else:
        print("\n-- Dimensoes do talhao (RETANGULO) --")
        dim1 = ler_float("Comprimento (m): ")
        dim2 = ler_float("Largura (m): ")
        dim3 = 0.0

    figura, area = calcular_area(cultura, dim1, dim2, dim3)

    print(f"\n-- Manejo de insumos para {cultura} --")
    produto = ler_texto("Produto a aplicar (ex: Fosfato, Ureia, Adubo NPK): ")
    dose = ler_float("Dose do produto (mL por metro de rua, ex: 500): ")
    ruas = ler_int("Numero de ruas da lavoura: ")
    comprimento_rua = ler_float("Comprimento de cada rua (m): ")

    total_insumo_l = calcular_insumo(dose, ruas, comprimento_rua)

    # Insercao nos vetores paralelos (mesma posicao/indice em todos)
    vet_cultura.append(cultura)
    vet_figura.append(figura)
    vet_dim1.append(dim1)
    vet_dim2.append(dim2)
    vet_dim3.append(dim3)
    vet_area_m2.append(area)
    vet_produto.append(produto)
    vet_dose_ml_m.append(dose)
    vet_ruas.append(ruas)
    vet_comprimento_rua_m.append(comprimento_rua)
    vet_total_insumo_l.append(total_insumo_l)

    indice = len(vet_cultura) - 1
    print(f"\n>> Registro cadastrado com sucesso no indice {indice}!")
    print(f"   Area de plantio: {area:.2f} m2  |  Insumo total: {total_insumo_l:.2f} L")


def listar_dados():
    """Saida de dados: imprime todos os registros no terminal."""
    print("\n=== SAIDA DE DADOS (todos os registros) ===")
    if not vet_cultura:
        print(">> Nenhum registro cadastrado ainda.")
        return

    for i in range(len(vet_cultura)):
        print(f"\n[{i}] Cultura: {vet_cultura[i]}  |  Figura: {vet_figura[i]}")
        if vet_figura[i] == "Trapezio":
            print(f"    Base maior: {vet_dim1[i]:.2f} m | Base menor: {vet_dim2[i]:.2f} m | Altura: {vet_dim3[i]:.2f} m")
        else:
            print(f"    Comprimento: {vet_dim1[i]:.2f} m | Largura: {vet_dim2[i]:.2f} m")
        print(f"    Area de plantio: {vet_area_m2[i]:.2f} m2")
        print(f"    Insumo: {vet_produto[i]} | Dose: {vet_dose_ml_m[i]:.2f} mL/m | "
              f"Ruas: {vet_ruas[i]} | Comprimento da rua: {vet_comprimento_rua_m[i]:.2f} m")
        print(f"    >> Total de insumo necessario: {vet_total_insumo_l[i]:.2f} litros")

    print(f"\nTotal de registros: {len(vet_cultura)}")


def atualizar_dados():
    """Atualizacao de dados numa posicao qualquer do vetor."""
    print("\n=== ATUALIZACAO DE DADOS ===")
    if not vet_cultura:
        print(">> Nenhum registro cadastrado ainda.")
        return

    listar_dados()
    indice = ler_int(f"\nDigite o indice do registro a atualizar (0 a {len(vet_cultura) - 1}): ") \
        if len(vet_cultura) > 0 else None

    if indice is None or indice < 0 or indice >= len(vet_cultura):
        print(">> Indice invalido.")
        return

    print(f"\nAtualizando registro [{indice}] - cultura atual: {vet_cultura[indice]}")
    cultura = escolher_cultura()

    if cultura == "Cafe":
        dim1 = ler_float("Nova base maior (m): ")
        dim2 = ler_float("Nova base menor (m): ")
        dim3 = ler_float("Nova altura (m): ")
    else:
        dim1 = ler_float("Novo comprimento (m): ")
        dim2 = ler_float("Nova largura (m): ")
        dim3 = 0.0

    figura, area = calcular_area(cultura, dim1, dim2, dim3)

    produto = ler_texto("Novo produto a aplicar: ")
    dose = ler_float("Nova dose (mL por metro de rua): ")
    ruas = ler_int("Novo numero de ruas: ")
    comprimento_rua = ler_float("Novo comprimento de cada rua (m): ")
    total_insumo_l = calcular_insumo(dose, ruas, comprimento_rua)

    # Atualiza a MESMA posicao em todos os vetores
    vet_cultura[indice] = cultura
    vet_figura[indice] = figura
    vet_dim1[indice] = dim1
    vet_dim2[indice] = dim2
    vet_dim3[indice] = dim3
    vet_area_m2[indice] = area
    vet_produto[indice] = produto
    vet_dose_ml_m[indice] = dose
    vet_ruas[indice] = ruas
    vet_comprimento_rua_m[indice] = comprimento_rua
    vet_total_insumo_l[indice] = total_insumo_l

    print(f"\n>> Registro [{indice}] atualizado com sucesso!")


def deletar_dados():
    """Delecao de dados do vetor numa posicao qualquer."""
    print("\n=== DELECAO DE DADOS ===")
    if not vet_cultura:
        print(">> Nenhum registro cadastrado ainda.")
        return

    listar_dados()
    indice = ler_int(f"\nDigite o indice do registro a deletar (0 a {len(vet_cultura) - 1}): ")

    if indice < 0 or indice >= len(vet_cultura):
        print(">> Indice invalido.")
        return

    confirmacao = input(f"Confirma a exclusao do registro [{indice}] ({vet_cultura[indice]})? (S/N): ").strip().upper()
    if confirmacao != "S":
        print(">> Operacao cancelada.")
        return

    # Remove a MESMA posicao em todos os vetores (mantem alinhamento)
    vet_cultura.pop(indice)
    vet_figura.pop(indice)
    vet_dim1.pop(indice)
    vet_dim2.pop(indice)
    vet_dim3.pop(indice)
    vet_area_m2.pop(indice)
    vet_produto.pop(indice)
    vet_dose_ml_m.pop(indice)
    vet_ruas.pop(indice)
    vet_comprimento_rua_m.pop(indice)
    vet_total_insumo_l.pop(indice)

    print(f"\n>> Registro [{indice}] removido com sucesso!")


def exportar_csv():
    """
    Exporta os vetores para um arquivo CSV (dados_agricolas.csv), que sera
    consumido pela aplicacao em R (calculo de media e desvio padrao).
    """
    print("\n=== EXPORTAR DADOS PARA CSV (uso na aplicacao R) ===")
    if not vet_cultura:
        print(">> Nenhum registro para exportar.")
        return

    with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "cultura", "figura", "dim1", "dim2", "dim3", "area_m2",
            "produto", "dose_ml_m", "ruas", "comprimento_rua_m", "total_insumo_l"
        ])
        for i in range(len(vet_cultura)):
            escritor.writerow([
                vet_cultura[i], vet_figura[i], vet_dim1[i], vet_dim2[i], vet_dim3[i],
                round(vet_area_m2[i], 4), vet_produto[i], vet_dose_ml_m[i], vet_ruas[i],
                vet_comprimento_rua_m[i], round(vet_total_insumo_l[i], 4)
            ])

    print(f">> Dados exportados com sucesso para: {CSV_PATH}")
    print(">> Use esse arquivo na aplicacao R (estatisticas.R) para calcular media e desvio padrao.")


def carregar_dados_exemplo():
    """Carrega alguns registros de exemplo para facilitar testes/demonstracao."""
    exemplos = [
        ("Cafe", 120.0, 90.0, 60.0, "Fosfato", 500.0, 10, 100.0),
        ("Cana-de-acucar", 200.0, 50.0, 0.0, "Ureia", 300.0, 15, 150.0),
    ]
    for cultura, d1, d2, d3, produto, dose, ruas, comp in exemplos:
        figura, area = calcular_area(cultura, d1, d2, d3)
        total = calcular_insumo(dose, ruas, comp)
        vet_cultura.append(cultura)
        vet_figura.append(figura)
        vet_dim1.append(d1)
        vet_dim2.append(d2)
        vet_dim3.append(d3)
        vet_area_m2.append(area)
        vet_produto.append(produto)
        vet_dose_ml_m.append(dose)
        vet_ruas.append(ruas)
        vet_comprimento_rua_m.append(comp)
        vet_total_insumo_l.append(total)


# ---------------------------------------------------------------------------
# Menu principal (item e) com loop e decisao (item f)
# ---------------------------------------------------------------------------
def exibir_menu():
    print("\n" + "=" * 55)
    print(" FARMTECH SOLUTIONS - GESTAO AGRICOLA DIGITAL")
    print("=" * 55)
    print(" 1 - Entrada de dados (cadastrar novo talhao)")
    print(" 2 - Saida de dados (listar todos os registros)")
    print(" 3 - Atualizar dados (numa posicao do vetor)")
    print(" 4 - Deletar dados (numa posicao do vetor)")
    print(" 5 - Exportar dados para CSV (para uso no R)")
    print(" 0 - Sair do programa")
    print("=" * 55)


def main():
    print("Bem-vindo ao sistema de gestao agricola da FarmTech Solutions!")

    # Comente a linha abaixo se nao quiser dados de exemplo pre-carregados.
    carregar_dados_exemplo()

    while True:  # loop principal do menu
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_dados()
        elif opcao == "2":
            listar_dados()
        elif opcao == "3":
            atualizar_dados()
        elif opcao == "4":
            deletar_dados()
        elif opcao == "5":
            exportar_csv()
        elif opcao == "0":
            print("\nEncerrando o programa. Ate logo!")
            break
        else:
            print(">> Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
