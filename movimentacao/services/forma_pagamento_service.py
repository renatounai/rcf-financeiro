from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import FORMA_PAGAMENTO_DESCRICAO_REPETIDA, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA
from movimentacao.models.forma_pagamento import FormaPagamento


def save(forma_pagamento: FormaPagamento) -> None:
    forma_pagamento.save()


def delete(forma_pagamento_id: int) -> None:
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    forma_pagamento.delete()


def _validate(forma_pagamento: FormaPagamento):
    if not forma_pagamento.descricao or not forma_pagamento.descricao.strip():
        raise MovimentacaoError(FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA)

    if not forma_pagamento.id:
        exists = FormaPagamento.objects.filter(descricao__iexact=forma_pagamento.descricao).exists()
        if exists:
            raise MovimentacaoError(FORMA_PAGAMENTO_DESCRICAO_REPETIDA)


@receiver(pre_save, sender=FormaPagamento)
def _before_save(instance: FormaPagamento, **_) -> None:
    _validate(instance)
