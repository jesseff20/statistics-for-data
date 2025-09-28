# -*- coding: utf-8 -*-
"""
Script para executar os loaders de dados e popular a pasta /data.
"""
from src.data import loaders
import os

# Pega o limite da variável de ambiente, com um padrão de 1000 para segurança
NYC_DATA_LIMIT = int(os.getenv("LIMIT", 500))

if __name__ == "__main__":
    print("--- Iniciando download dos datasets ---")
    loaders.load_california_housing()
    print("-" * 20)
    # Para o dataset de NYC, usamos um limite pequeno para o teste inicial
    loaders.load_nyc_311(limit=NYC_DATA_LIMIT)
    print("--- Download concluído com sucesso! ---")
