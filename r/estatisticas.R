# ============================================================================
# FarmTech Solutions - Estatisticas basicas em R
# ============================================================================
# Le o CSV exportado pela aplicacao Python (dados_agricolas.csv) e calcula
# estatisticas basicas (media e desvio padrao) da area de plantio e do total
# de insumo utilizado, tanto de forma geral quanto por cultura.
#
# Como executar:
#   Rscript estatisticas.R
#   ou, dentro de um R interativo: source("estatisticas.R")
#
# Observacao: por padrao o script procura o arquivo "dados_agricolas.csv" na
# pasta "python/" um nivel acima (../python/dados_agricolas.csv), que e onde
# a aplicacao Python grava o export (opcao 5 do menu). Ajuste o caminho
# abaixo se necessario, ou passe o caminho como argumento de linha de
# comando: Rscript estatisticas.R caminho/para/dados_agricolas.csv
# ============================================================================

args <- commandArgs(trailingOnly = TRUE)

if (length(args) >= 1) {
  caminho_csv <- args[1]
} else {
  caminho_csv <- file.path("..", "python", "dados_agricolas.csv")
}

if (!file.exists(caminho_csv)) {
  cat("ERRO: arquivo nao encontrado em:", caminho_csv, "\n")
  cat("Gere o arquivo primeiro na aplicacao Python (menu, opcao 5 - Exportar dados para CSV)\n")
  cat("ou informe o caminho correto: Rscript estatisticas.R caminho/para/dados_agricolas.csv\n")
  quit(status = 1)
}

dados <- read.csv(caminho_csv, stringsAsFactors = FALSE)

cat("============================================================\n")
cat(" FARMTECH SOLUTIONS - ESTATISTICAS DA LAVOURA (R)\n")
cat("============================================================\n")
cat("Arquivo lido:", caminho_csv, "\n")
cat("Total de registros:", nrow(dados), "\n")

if (nrow(dados) == 0) {
  cat("\nNenhum registro para analisar.\n")
  quit(status = 0)
}

# ----------------------------------------------------------------------------
# Funcao auxiliar: calcula e imprime media e desvio padrao de uma coluna
# ----------------------------------------------------------------------------
imprimir_estatisticas <- function(valores, titulo, unidade) {
  media <- mean(valores)
  desvio <- if (length(valores) > 1) sd(valores) else 0
  minimo <- min(valores)
  maximo <- max(valores)
  cat(sprintf("\n-- %s --\n", titulo))
  cat(sprintf("  Media...........: %.2f %s\n", media, unidade))
  cat(sprintf("  Desvio padrao...: %.2f %s\n", desvio, unidade))
  cat(sprintf("  Minimo..........: %.2f %s\n", minimo, unidade))
  cat(sprintf("  Maximo..........: %.2f %s\n", maximo, unidade))
}

# ----------------------------------------------------------------------------
# Estatisticas gerais (todas as culturas juntas)
# ----------------------------------------------------------------------------
cat("\n============================================================\n")
cat(" ESTATISTICAS GERAIS (todas as culturas)\n")
cat("============================================================\n")
imprimir_estatisticas(dados$area_m2, "Area de plantio", "m2")
imprimir_estatisticas(dados$total_insumo_l, "Total de insumo aplicado", "litros")

# ----------------------------------------------------------------------------
# Estatisticas por cultura (usando funcoes base do R: tapply / split)
# ----------------------------------------------------------------------------
cat("\n============================================================\n")
cat(" ESTATISTICAS POR CULTURA\n")
cat("============================================================\n")

culturas <- unique(dados$cultura)

for (cultura_atual in culturas) {
  subset_dados <- dados[dados$cultura == cultura_atual, ]
  cat(sprintf("\n>>> Cultura: %s (n = %d registros)\n", cultura_atual, nrow(subset_dados)))
  imprimir_estatisticas(subset_dados$area_m2, "  Area de plantio", "m2")
  imprimir_estatisticas(subset_dados$total_insumo_l, "  Total de insumo aplicado", "litros")
}

# ----------------------------------------------------------------------------
# Resumo consolidado usando tapply (media e desvio por cultura, de uma vez)
# ----------------------------------------------------------------------------
cat("\n============================================================\n")
cat(" RESUMO CONSOLIDADO (tapply)\n")
cat("============================================================\n")

media_area_por_cultura <- tapply(dados$area_m2, dados$cultura, mean)
sd_area_por_cultura <- tapply(dados$area_m2, dados$cultura, function(x) if (length(x) > 1) sd(x) else 0)
media_insumo_por_cultura <- tapply(dados$total_insumo_l, dados$cultura, mean)
sd_insumo_por_cultura <- tapply(dados$total_insumo_l, dados$cultura, function(x) if (length(x) > 1) sd(x) else 0)

cat("\nMedia de area (m2) por cultura:\n")
print(round(media_area_por_cultura, 2))
cat("\nDesvio padrao de area (m2) por cultura:\n")
print(round(sd_area_por_cultura, 2))
cat("\nMedia de insumo (litros) por cultura:\n")
print(round(media_insumo_por_cultura, 2))
cat("\nDesvio padrao de insumo (litros) por cultura:\n")
print(round(sd_insumo_por_cultura, 2))

cat("\n============================================================\n")
cat(" Fim da analise estatistica.\n")
cat("============================================================\n")
