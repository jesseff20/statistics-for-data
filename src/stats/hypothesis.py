# -*- coding: utf-8 -*-
"""
Módulo com implementações de testes de hipóteses.

Este script serve como um wrapper para as funções de testes
estatísticos da biblioteca SciPy, facilitando seu uso e
validação cruzada.
"""
import numpy as np
from scipy import stats


def two_sample_ttest(a: np.ndarray, b: np.ndarray, equal_var: bool = False):
    """
    Executa um teste t de duas amostras independentes.

    Args:
        a (np.ndarray): Amostra 1.
        b (np.ndarray): Amostra 2.
        equal_var (bool): Se True, assume variâncias iguais (teste de Student).
                          Se False, não assume (teste de Welch).

    Returns:
        tuple: Estatística do teste e p-valor.
    """
    return stats.ttest_ind(a, b, equal_var=equal_var)


def chi_square_independence(table: np.ndarray):
    """
    Executa o teste Qui-quadrado de independência em uma tabela de contingência.

    Args:
        table (np.ndarray): Tabela de contingência 2D.

    Returns:
        tuple: Estatística qui-quadrado, p-valor, graus de liberdade,
               frequências esperadas e resíduos padronizados.
    """
    chi2, p, dof, expected = stats.chi2_contingency(table)

    # Calcula os resíduos padronizados para identificar as células com maior desvio
    residuals = (table - expected) / np.sqrt(expected)

    return chi2, p, dof, expected, residuals
