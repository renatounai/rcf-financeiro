from django.test import SimpleTestCase

from movimentacao.models.pessoa import Pessoa
from utils.model_utils import is_model_empty


class TestModelUtils(SimpleTestCase):
    def test_is_model_not_empty(self):
        model = Pessoa(id=1)
        self.assertFalse(is_model_empty(model))