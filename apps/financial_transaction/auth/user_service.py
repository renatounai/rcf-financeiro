from django.contrib.auth.models import User

from apps.financial_transaction.exceptions.FinancialTransactionError import FinancialTransactionError


def create_account(user: User) -> User:
    """
    Cria um usuário. O email servirá como username
    """

    if not user.password:
        raise FinancialTransactionError("A senha é obrigatória!")

    if not user.email:
        raise FinancialTransactionError("O e-email é obrigatório!")

    if User.objects.filter(username__iexact=user.email).exists():
        raise FinancialTransactionError("Já existe um usuário com este e-mail!")

    return User.objects.create_user(user.email, user.email, user.password)




