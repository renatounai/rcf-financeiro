from movimentacao.models.movimentacao_financeira import MovimentacaoFinanceira


def save(movimentacao_financeira: MovimentacaoFinanceira):
    movimentacao_financeira.full_clean()
    movimentacao_financeira.save()
