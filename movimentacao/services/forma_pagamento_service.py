from django.shortcuts import get_object_or_404

from movimentacao.exceptions.movimentacao_error import MovimentacaoErro
from movimentacao.models.forma_pagamento import FormaPagamento


def _validate(forma_pagamento: FormaPagamento) -> None:
    if not forma_pagamento.descricao or not forma_pagamento.descricao.strip():
        raise MovimentacaoErro("A descrição da forma de pagamento é obrigatória!")


def save(forma_pagamento: FormaPagamento) -> None:
    _validate(forma_pagamento)
    forma_pagamento.save()


def delete(forma_pagamento_id: int):
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    forma_pagamento.delete()
