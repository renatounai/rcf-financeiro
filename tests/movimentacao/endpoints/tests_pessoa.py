from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from movimentacao.endpoints.pessoa_rest import PessoaIn
from movimentacao.models.pessoa import Pessoa

APPLICATION_JSON = "application/json"


class PessoaTest(TestCase):

    def test_should_get_all_pessoas(self):
        Pessoa.objects.create(nome="Renato")
        Pessoa.objects.create(nome="Ellen")

        response = self.client.get("/api/pessoas/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["nome"], "Renato")
        self.assertEqual(formas[1]["nome"], "Ellen")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/pessoas/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_pessoa_only_name(self):
        pessoa = Pessoa.objects.create(nome="Renato")

        response = self.client.get(f"/api/pessoas/{pessoa.id}")

        pessoa = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pessoa["nome"], "Renato")
        self.assertEqual(pessoa["email"], None)
        self.assertEqual(pessoa["instagram_user"], None)
        self.assertEqual(pessoa["facebook_user"], None)
        self.assertEqual(pessoa["fone"], None)

    def test_shoud_get_a_pessoa_all_fields(self):
        pessoa = Pessoa.objects.create(nome="Renato",
                                       email="renatomcn@gmail.com",
                                       instagram_user="renatounai",
                                       facebook_user="renatounaif",
                                       fone="38988075494")

        response = self.client.get(f"/api/pessoas/{pessoa.id}")

        pessoa = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pessoa["nome"], "Renato")
        self.assertEqual(pessoa["email"], "renatomcn@gmail.com")
        self.assertEqual(pessoa["instagram_user"], "renatounai")
        self.assertEqual(pessoa["facebook_user"], "renatounaif")
        self.assertEqual(pessoa["fone"], "38988075494")

    def test_should_create_a_pessoa_only_name(self):
        pessoa = PessoaIn(nome="Renato")

        response = self.client.post("/api/pessoas/", pessoa.__dict__, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pessoa.objects.count(), 1)

    def test_should_create_a_pessoa_all_fields(self):
        pessoa = PessoaIn(nome="Renato",
                          email="renatomcn@gmail.com",
                          fone="38988075494",
                          instagram_user="renatounai",
                          facebook_user="renatounaif")

        response = self.client.post("/api/pessoas/", pessoa.__dict__, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pessoa.objects.count(), 1)

    def test_should_raise_error_if_email_is_invalid(self):
        pessoa = {"nome": "Renato", "email": "renato"}
        response = self.client.post("/api/pessoas/", pessoa, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)

    def test_shoud_remove_domain_from_social_media_ids_without_query_string(self):
        pessoa = PessoaIn(nome="Renato",
                          email="renatomcn@gmail.com",
                          fone="38988075494",
                          instagram_user="https://instagram.com.br/renatounai",
                          facebook_user="https://facebook.com/renatounaif")

        self._validate_social_media(pessoa)

    def test_shoud_remove_domain_from_social_media_ids_with_query_string(self):
        pessoa = PessoaIn(nome="Renato",
                          email="renatomcn@gmail.com",
                          fone="38988075494",
                          instagram_user="https://instagram.com.br/renatounai?algo",
                          facebook_user="https://facebook.com/renatounaif?parameter=teste&other=1")

        self._validate_social_media(pessoa)

    def _validate_social_media(self, pessoa):
        response = self.client.post("/api/pessoas/", pessoa.__dict__, content_type=APPLICATION_JSON)
        pessoa_saved = response.json()
        Pessoa.objects.get(pk=pessoa_saved["id"])
        self.assertEqual("renatounai", pessoa_saved["instagram_user"])
        self.assertEqual("renatounaif", pessoa_saved["facebook_user"])

    def test_shoud_update_a_pessoa(self):
        pessoa = Pessoa.objects.create(nome="Renato")

        response = self.client.put(f"/api/pessoas/{pessoa.id}", {"nome": "Kalel"}, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        pessoa = Pessoa.objects.get(pk=pessoa.id)

        self.assertEqual(pessoa.nome, "Kalel")

    def test_shoud_delete_a_pessoa(self):
        pessoa = Pessoa.objects.create(nome="Renato")

        response = self.client.delete(f"/api/pessoas/{pessoa.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            Pessoa.objects.get(pk=1)
