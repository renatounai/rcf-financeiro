from movimentacao.messages import FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, FORMA_PAGAMENTO_DESCRICAO_REPETIDA
from movimentacao.models.forma_pagamento import FormaPagamento
from movimentacao.services.base import validate_description


def save(forma_pagamento: FormaPagamento):
    validate_description(forma_pagamento, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA, FORMA_PAGAMENTO_DESCRICAO_REPETIDA)

    forma_pagamento.full_clean()
    forma_pagamento.save()
