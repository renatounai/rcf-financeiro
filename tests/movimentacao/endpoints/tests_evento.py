# from django.core.exceptions import ObjectDoesNotExist
# from django.test import TestCase
#
# from movimentacao.endpoints.pessoa_rest import PessoaIn
# from movimentacao.models.evento import Evento
# from movimentacao.models.pessoa import Pessoa
# from movimentacao.models.status_evento import StatusEvento
#
# APPLICATION_JSON = "application/json"
#
#
# class EventoTest(TestCase):
#
#     def test_should_get_all_eventos(self):
#         pessoa = Pessoa(nome="Renato")
#         pessoa.save()
#
#         evento_in = {
#             "quitado": False,
#             "status": StatusEvento.NEGOCIANDO,
#             "gratuito": False,
#             "cliente_id": pessoa.id
#         }
#
#         response = self.client.post("/api/eventos/", evento_in, content_type=APPLICATION_JSON)
#
#         print(response.status_code)
#         self.assertEqual(response.status_code, 204)
