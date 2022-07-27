from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from apps.financial_transaction.endpoints.person_rest import PersonIn
from apps.financial_transaction.messages import PESSOA_NOME_OBRIGATORIO
from apps.financial_transaction.models.person import Person

APPLICATION_JSON = "application/json"


class PersonTest(TestCase):

    def setUp(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer 123"

    def test_should_get_all_persons(self):
        Person.objects.create(name="Renato")
        Person.objects.create(name="Ellen")

        response = self.client.get("/api/persons/")
        formas = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(formas), 2)

        self.assertEqual(formas[0]["name"], "Renato")
        self.assertEqual(formas[1]["name"], "Ellen")

    def test_shoud_return_empty_if_nothing_found(self):
        response = self.client.get("/api/persons/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_shoud_get_a_person_only_name(self):
        person = Person.objects.create(name="Renato")

        response = self.client.get(f"/api/persons/{person.id}")

        person = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(person["name"], "Renato")
        self.assertEqual(person["email"], None)
        self.assertEqual(person["instagram_user"], None)
        self.assertEqual(person["facebook_user"], None)
        self.assertEqual(person["phone"], None)

    def test_shoud_get_a_person_all_fields(self):
        person = Person.objects.create(name="Renato",
                                       email="renatomcn@gmail.com",
                                       instagram_user="renatounai",
                                       facebook_user="renatounaif",
                                       phone="38988075494")

        response = self.client.get(f"/api/persons/{person.id}")

        person = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(person["name"], "Renato")
        self.assertEqual(person["email"], "renatomcn@gmail.com")
        self.assertEqual(person["instagram_user"], "renatounai")
        self.assertEqual(person["facebook_user"], "renatounaif")
        self.assertEqual(person["phone"], "38988075494")

    def test_should_create_a_person_only_name(self):
        person = PersonIn(name="Renato")

        response = self.client.post("/api/persons/", person.__dict__, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Person.objects.count(), 1)

    def test_should_create_a_person_all_fields(self):
        person = PersonIn(name="Renato",
                          email="renatomcn@gmail.com",
                          phone="38988075494",
                          instagram_user="renatounai",
                          facebook_user="renatounaif")

        response = self.client.post("/api/persons/", person.__dict__, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Person.objects.count(), 1)

    def test_should_raise_error_if_name_is_blank(self):
        person = {"name": ""}
        response = self.client.post("/api/persons/", person, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'], PESSOA_NOME_OBRIGATORIO)

    def test_should_raise_error_if_name_is_white_space(self):
        person = {"name": "    "}
        response = self.client.post("/api/persons/", person, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()['detail'], PESSOA_NOME_OBRIGATORIO)

    def test_should_raise_error_if_email_is_invalid(self):
        person = {"name": "Renato", "email": "renato"}
        response = self.client.post("/api/persons/", person, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 422)

    def test_shoud_remove_domain_from_social_media_ids_without_query_string(self):
        person = PersonIn(name="Renato",
                          email="renatomcn@gmail.com",
                          phone="38988075494",
                          instagram_user="https://instagram.com.br/renatounai",
                          facebook_user="https://facebook.com/renatounaif")

        self._validate_social_media(person)

    def test_shoud_remove_domain_from_social_media_ids_with_query_string(self):
        person = PersonIn(name="Renato",
                          email="renatomcn@gmail.com",
                          phone="38988075494",
                          instagram_user="https://instagram.com.br/renatounai?algo",
                          facebook_user="https://facebook.com/renatounaif?parameter=teste&other=1")

        self._validate_social_media(person)

    def _validate_social_media(self, person):
        response = self.client.post("/api/persons/", person.__dict__, content_type=APPLICATION_JSON)
        person_saved = response.json()
        Person.objects.get(pk=person_saved["id"])
        self.assertEqual("renatounai", person_saved["instagram_user"])
        self.assertEqual("renatounaif", person_saved["facebook_user"])

    def test_shoud_update_a_person(self):
        person = Person.objects.create(name="Renato")

        response = self.client.put(f"/api/persons/{person.id}", {"name": "Kalel"}, content_type=APPLICATION_JSON)
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(pk=person.id)

        self.assertEqual(person.name, "Kalel")

    def test_shoud_delete_a_person(self):
        person = Person.objects.create(name="Renato")

        response = self.client.delete(f"/api/persons/{person.id}")
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            Person.objects.get(pk=1)
