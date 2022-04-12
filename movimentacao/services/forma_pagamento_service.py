from movimentacao.models.forma_pagamento import FormaPagamento


def save(forma_pagamento: FormaPagamento):
    forma_pagamento.full_clean()
    forma_pagamento.save()
