from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.messages import JA_EXISTE_FORMA_PAGAMENTO_COM_ESTA_DESCRICAO, FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA
from movimentacao.models.forma_pagamento import FormaPagamento


def delete(forma_pagamento_id: int) -> None:
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    forma_pagamento.delete()


@receiver(pre_save, sender=FormaPagamento)
def _before_save(instance: FormaPagamento, **_) -> None:
    if not instance.descricao or not instance.descricao.strip():
        raise MovimentacaoError(FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA)

    if not instance.id:
        exists = FormaPagamento.objects.filter(descricao__iexact=instance.descricao).exists()
        if exists:
            raise MovimentacaoError(JA_EXISTE_FORMA_PAGAMENTO_COM_ESTA_DESCRICAO)
