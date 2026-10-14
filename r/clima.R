# ============================================================================
# FarmTech Solutions - Consulta de dados meteorologicos (Ir Alem)
# ============================================================================
# Conecta-se a uma API meteorologica publica e gratuita (Open-Meteo,
# https://open-meteo.com) - NAO exige chave de API/cadastro - para coletar
# a previsao do tempo atual e dos proximos dias de uma localidade da lavoura,
# processa a resposta (JSON) e exibe as informacoes em texto simples no
# terminal.
#
# Pacotes necessarios (instalar uma unica vez):
#   install.packages("httr")
#   install.packages("jsonlite")
#
# Como executar (usa Piracicaba/SP como padrao, regiao de referencia para
# cafe e cana-de-acucar):
#   Rscript clima.R
#
# Para consultar outra localidade, informe latitude e longitude como
# argumentos de linha de comando:
#   Rscript clima.R -22.9068 -43.1729
# ============================================================================

if (!requireNamespace("httr", quietly = TRUE)) {
  stop("Pacote 'httr' nao encontrado. Instale com: install.packages(\"httr\")")
}
if (!requireNamespace("jsonlite", quietly = TRUE)) {
  stop("Pacote 'jsonlite' nao encontrado. Instale com: install.packages(\"jsonlite\")")
}

library(httr)
library(jsonlite)

args <- commandArgs(trailingOnly = TRUE)

# Coordenadas padrao: Piracicaba - SP (regiao de referencia para cana e cafe)
latitude <- -22.7253
longitude <- -47.6492
nome_local <- "Piracicaba - SP (padrao)"

if (length(args) >= 2) {
  latitude <- as.numeric(args[1])
  longitude <- as.numeric(args[2])
  nome_local <- sprintf("Latitude %.4f, Longitude %.4f", latitude, longitude)
}

# Traducao simples dos codigos de tempo (weathercode) da Open-Meteo (WMO)
descrever_tempo <- function(codigo) {
  descricoes <- c(
    "0" = "Ceu limpo",
    "1" = "Predominante limpo",
    "2" = "Parcialmente nublado",
    "3" = "Nublado",
    "45" = "Nevoeiro",
    "48" = "Nevoeiro com deposito de gelo",
    "51" = "Garoa fraca",
    "53" = "Garoa moderada",
    "55" = "Garoa forte",
    "61" = "Chuva fraca",
    "63" = "Chuva moderada",
    "65" = "Chuva forte",
    "71" = "Neve fraca",
    "80" = "Pancadas de chuva fracas",
    "81" = "Pancadas de chuva moderadas",
    "82" = "Pancadas de chuva fortes",
    "95" = "Tempestade"
  )
  chave <- as.character(codigo)
  if (chave %in% names(descricoes)) {
    return(descricoes[[chave]])
  }
  return(paste("Codigo de tempo:", codigo))
}

cat("============================================================\n")
cat(" FARMTECH SOLUTIONS - DADOS METEOROLOGICOS (API PUBLICA)\n")
cat("============================================================\n")
cat("Local consultado:", nome_local, "\n")
cat("Fonte dos dados.: Open-Meteo (https://open-meteo.com)\n")
cat("------------------------------------------------------------\n")

url_base <- "https://api.open-meteo.com/v1/forecast"

resposta <- tryCatch({
  GET(
    url_base,
    query = list(
      latitude = latitude,
      longitude = longitude,
      current_weather = "true",
      daily = "temperature_2m_max,temperature_2m_min,precipitation_sum",
      timezone = "America/Sao_Paulo"
    ),
    timeout(15)
  )
}, error = function(e) {
  cat("\nERRO: nao foi possivel conectar a API meteorologica.\n")
  cat("Detalhe:", conditionMessage(e), "\n")
  cat("Verifique sua conexao com a internet e tente novamente.\n")
  quit(status = 1)
})

if (status_code(resposta) != 200) {
  cat("\nERRO: a API retornou o status HTTP", status_code(resposta), "\n")
  quit(status = 1)
}

conteudo_texto <- content(resposta, as = "text", encoding = "UTF-8")
dados_clima <- fromJSON(conteudo_texto)

# -------------------- Condicoes atuais --------------------
atual <- dados_clima$current_weather

cat("\n>> CONDICOES ATUAIS\n")
cat(sprintf("   Temperatura........: %.1f C\n", atual$temperature))
cat(sprintf("   Velocidade do vento: %.1f km/h\n", atual$windspeed))
cat(sprintf("   Direcao do vento...: %.0f graus\n", atual$winddirection))
cat(sprintf("   Condicao...........: %s\n", descrever_tempo(atual$weathercode)))
cat(sprintf("   Hora da leitura....: %s\n", atual$time))

# -------------------- Previsao diaria --------------------
diario <- dados_clima$daily

cat("\n>> PREVISAO DOS PROXIMOS DIAS\n")
for (i in seq_along(diario$time)) {
  cat(sprintf(
    "   %s | Min: %5.1f C | Max: %5.1f C | Chuva prevista: %5.1f mm\n",
    diario$time[i],
    diario$temperature_2m_min[i],
    diario$temperature_2m_max[i],
    diario$precipitation_sum[i]
  ))
}

# -------------------- Alerta simples para o agronegocio --------------------
cat("\n>> ALERTA PARA O MANEJO DA LAVOURA\n")
chuva_hoje <- diario$precipitation_sum[1]
if (chuva_hoje >= 10) {
  cat("   Previsao de chuva significativa hoje: evite pulverizacao de insumos.\n")
} else if (atual$windspeed >= 20) {
  cat("   Vento forte: cuidado com deriva na pulverizacao de defensivos.\n")
} else {
  cat("   Condicoes favoraveis para operacoes de campo (pulverizacao/plantio).\n")
}

cat("\n============================================================\n")
cat(" Fim da consulta meteorologica.\n")
cat("============================================================\n")
