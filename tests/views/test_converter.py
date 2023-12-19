from django.urls import reverse

from tests.handler import ViewTestCase


class ClientsViewTestCase(ViewTestCase):
    def test_valid_currency_converter(self):
        self.login_user()
        response = self.client.post(
            reverse("converter dashboard"),
            {
                "currency_from": "EUR",
                "amount_from": 10,
                "currency_to": "USD",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_from_currency_converter(self):
        self.login_user()
        response = self.client.post(
            reverse("converter dashboard"),
            {
                "currency_from": "TEST",
                "amount_from": 10,
                "currency_to": "USD",
            },
        )
        self.assertEqual(response.status_code, 400)


    def test_invalid_to_currency_converter(self):
        self.login_user()
        response = self.client.post(
            reverse("converter dashboard"),
            {
                "currency_from": "EUR",
                "amount_from": 10,
                "currency_to": "TEST",
            },
        )
        self.assertEqual(response.status_code, 400)


    def test_invalid_negative_amount_from_currency_converter(self):
        self.login_user()
        response = self.client.post(
            reverse("converter dashboard"),
            {
                "currency_from": "EUR",
                "amount_from": -10,
                "currency_to": "USD",
            },
        )
        self.assertEqual(response.status_code, 400)


    def test_invalid_amount_from_currency_converter(self):
        self.login_user()
        response = self.client.post(
            reverse("converter dashboard"),
            {
                "currency_from": "EUR",
                "amount_from": "TEST",
                "currency_to": "USD",
            },
        )
        self.assertEqual(response.status_code, 400)


    def test_unauthenticated_user_converter(self):
        response = self.client.post(
            reverse("converter dashboard"),
            {
                "currency_from": "EUR",
                "amount_from": 10,
                "currency_to": "USD",
            },
        )
        self.assertEqual(response.status_code, 302)