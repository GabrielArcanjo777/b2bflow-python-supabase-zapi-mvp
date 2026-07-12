import base64
import json
import os
import unittest
from unittest.mock import Mock, patch

import main


def jwt_with_role(role: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"role": role}).encode()).decode()
    return f"header.{payload.rstrip('=')}.signature"


class EnvironmentTests(unittest.TestCase):
    def test_boolean_values_are_parsed_explicitly(self) -> None:
        for value in ("true", "1", "yes", "sim"):
            with (
                self.subTest(value=value),
                patch.dict(os.environ, {"FLAG": value}, clear=True),
            ):
                self.assertTrue(main.get_bool_env("FLAG", default=False))

        for value in ("false", "0", "no", "não"):
            with (
                self.subTest(value=value),
                patch.dict(os.environ, {"FLAG": value}, clear=True),
            ):
                self.assertFalse(main.get_bool_env("FLAG", default=True))

    def test_invalid_boolean_fails_closed(self) -> None:
        with patch.dict(os.environ, {"DRY_RUN": "treu"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "booleano explícito"):
                main.get_bool_env("DRY_RUN", default=True)

    def test_publishable_and_anon_keys_are_rejected(self) -> None:
        for key in ("sb_publishable_example", jwt_with_role("anon")):
            with self.subTest(key=key):
                with self.assertRaisesRegex(RuntimeError, "publishable/anon"):
                    main.validate_supabase_backend_key(key)

    def test_live_send_requires_exact_confirmation(self) -> None:
        for value in ("", "yes", "i_understand", "I UNDERSTAND"):
            with (
                self.subTest(value=value),
                patch.dict(os.environ, {"LIVE_SEND_CONFIRM": value}, clear=True),
            ):
                with self.assertRaisesRegex(RuntimeError, "Envio real bloqueado"):
                    main.require_live_send_confirmation()

        with patch.dict(
            os.environ,
            {"LIVE_SEND_CONFIRM": main.LIVE_SEND_CONFIRMATION},
            clear=True,
        ):
            main.require_live_send_confirmation()


class ContactTests(unittest.TestCase):
    @patch("main.requests.get")
    def test_fetch_contacts_applies_server_limit_and_order(self, get: Mock) -> None:
        response = Mock(ok=True, status_code=200)
        response.json.return_value = [
            {"nome": "Ana", "telefone": "+55 (21) 99999-0000"},
            {"nome": "Beto", "telefone": "5521888880000"},
        ]
        get.return_value = response

        contacts = main.fetch_contacts(
            supabase_url="https://example.supabase.co",
            supabase_key="sb_secret_example",
            table_name="contacts",
            limit=2,
            timeout=10,
        )

        self.assertEqual([contact.nome for contact in contacts], ["Ana", "Beto"])
        self.assertEqual(
            get.call_args.kwargs["params"],
            {
                "select": "nome,telefone",
                "limit": 2,
                "order": "created_at.asc",
            },
        )

    @patch("main.send_text_message")
    @patch("main.fetch_contacts")
    @patch("main.load_dotenv")
    def test_invalid_dry_run_never_fetches_or_sends(
        self,
        load_dotenv: Mock,
        fetch_contacts: Mock,
        send_text_message: Mock,
    ) -> None:
        environment = {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_KEY": "sb_secret_example",
            "DRY_RUN": "treu",
        }
        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaises(RuntimeError):
                main.main()

        load_dotenv.assert_called_once()
        fetch_contacts.assert_not_called()
        send_text_message.assert_not_called()


if __name__ == "__main__":
    unittest.main()
