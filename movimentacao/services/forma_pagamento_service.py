from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save

from movimentacao.exceptions.movimentacao_error import MovimentacaoError
from movimentacao.models.forma_pagamento import FormaPagamento

JA_EXISTE_FORMA_PAGAMENTO_COM_ESTA_DESCRICAO = "Já existe uma forma de pagamento com esta descrição!"
FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA = "A descrição da forma de pagamento é obrigatória!"


def delete(forma_pagamento_id: int) -> None:
    forma_pagamento = get_object_or_404(FormaPagamento, id=forma_pagamento_id)
    forma_pagamento.delete()


@receiver(pre_save, sender=FormaPagamento)
def _before_save(instance: FormaPagamento, **_) -> None:
    if not instance.descricao or not instance.descricao.strip():
        raise MovimentacaoError(FORMA_PAGAMENTO_DESCRICAO_OBRIGATORIA)

    count = FormaPagamento.objects.filter(descricao__iexact=instance.descricao).count()
    if count > 0:
        raise MovimentacaoError(JA_EXISTE_FORMA_PAGAMENTO_COM_ESTA_DESCRICAO)
