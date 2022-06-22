from django.contrib.auth.models import User

from movimentacao.exceptions.MovimentacaoError import MovimentacaoError


def create_account(user: User) -> User:
    """
    Cria um usuário. O email servirá como username
    """

    if not user.password:
        raise MovimentacaoError("A senha é obrigatória!")

    if not user.email:
        raise MovimentacaoError("O e-email é obrigatório!")

    if User.objects.filter(username=user.email).exists():
        raise MovimentacaoError("Já existe um usuário com este e-mail!")

    return User.objects.create_user(user.email, user.email, user.password)




