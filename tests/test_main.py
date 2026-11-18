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


class RetryTests(unittest.TestCase):
    @patch("main.time.sleep")
    @patch("main.requests.post")
    def test_retries_transient_status_then_succeeds(self, post: Mock, sleep: Mock) -> None:
        post.side_effect = [
            Mock(ok=False, status_code=503),
            Mock(ok=False, status_code=429),
            Mock(ok=True, status_code=200),
        ]

        main.send_text_message(
            instance_id="i",
            token="t",
            client_token="c",
            phone="5521999990000",
            message="oi",
            timeout=5,
            max_attempts=3,
            backoff_seconds=0.5,
        )

        self.assertEqual(post.call_count, 3)
        # 0.5 na primeira espera, 1.0 na segunda (backoff exponencial).
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [0.5, 1.0])

    @patch("main.time.sleep")
    @patch("main.requests.post")
    def test_does_not_retry_client_error(self, post: Mock, sleep: Mock) -> None:
        post.return_value = Mock(ok=False, status_code=400)

        with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
            main.send_text_message(
                instance_id="i",
                token="t",
                client_token="c",
                phone="5521999990000",
                message="oi",
                timeout=5,
            )

        self.assertEqual(post.call_count, 1)
        sleep.assert_not_called()

    @patch("main.time.sleep")
    @patch("main.requests.post")
    def test_gives_up_after_max_attempts(self, post: Mock, sleep: Mock) -> None:
        post.return_value = Mock(ok=False, status_code=502)

        with self.assertRaisesRegex(RuntimeError, "após 2 tentativa"):
            main.send_text_message(
                instance_id="i",
                token="t",
                client_token="c",
                phone="5521999990000",
                message="oi",
                timeout=5,
                max_attempts=2,
                backoff_seconds=0.1,
            )

        self.assertEqual(post.call_count, 2)


class DeliveryTests(unittest.TestCase):
    @patch("main.requests.get")
    def test_known_phone_is_reported_as_delivered(self, get: Mock) -> None:
        get.return_value = Mock(ok=True, status_code=200)
        get.return_value.json.return_value = [{"phone": "5521999990000"}]

        self.assertTrue(
            main.was_delivered(
                supabase_url="https://example.supabase.co",
                supabase_key="sb_secret_example",
                table_name="deliveries",
                phone="5521999990000",
                timeout=5,
            )
        )

    @patch("main.requests.get")
    def test_unknown_phone_is_not_delivered(self, get: Mock) -> None:
        get.return_value = Mock(ok=True, status_code=200)
        get.return_value.json.return_value = []

        self.assertFalse(
            main.was_delivered(
                supabase_url="https://example.supabase.co",
                supabase_key="sb_secret_example",
                table_name="deliveries",
                phone="5521999990000",
                timeout=5,
            )
        )

    @patch("main.requests.get")
    def test_missing_delivery_table_fails_loudly(self, get: Mock) -> None:
        get.return_value = Mock(ok=False, status_code=404)

        with self.assertRaisesRegex(RuntimeError, "setup.sql"):
            main.was_delivered(
                supabase_url="https://example.supabase.co",
                supabase_key="sb_secret_example",
                table_name="deliveries",
                phone="5521999990000",
                timeout=5,
            )

    @patch("main.time.sleep")
    @patch("main.mark_delivered")
    @patch("main.was_delivered")
    @patch("main.send_text_message")
    @patch("main.fetch_contacts")
    @patch("main.load_dotenv")
    def test_already_delivered_contact_is_skipped(
        self,
        load_dotenv: Mock,
        fetch_contacts: Mock,
        send_text_message: Mock,
        was_delivered: Mock,
        mark_delivered: Mock,
        sleep: Mock,
    ) -> None:
        fetch_contacts.return_value = [main.Contact(nome="Ana", telefone="5521999990000")]
        was_delivered.return_value = True

        environment = {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_KEY": "sb_secret_example",
            "DRY_RUN": "false",
            "LIVE_SEND_CONFIRM": main.LIVE_SEND_CONFIRMATION,
            "ZAPI_INSTANCE_ID": "i",
            "ZAPI_TOKEN": "t",
            "ZAPI_CLIENT_TOKEN": "c",
        }
        with patch.dict(os.environ, environment, clear=True):
            main.main()

        send_text_message.assert_not_called()
        mark_delivered.assert_not_called()

    @patch("main.time.sleep")
    @patch("main.mark_delivered")
    @patch("main.was_delivered")
    @patch("main.send_text_message")
    @patch("main.fetch_contacts")
    @patch("main.load_dotenv")
    def test_successful_send_is_recorded(
        self,
        load_dotenv: Mock,
        fetch_contacts: Mock,
        send_text_message: Mock,
        was_delivered: Mock,
        mark_delivered: Mock,
        sleep: Mock,
    ) -> None:
        fetch_contacts.return_value = [main.Contact(nome="Ana", telefone="5521999990000")]
        was_delivered.return_value = False

        environment = {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_KEY": "sb_secret_example",
            "DRY_RUN": "false",
            "LIVE_SEND_CONFIRM": main.LIVE_SEND_CONFIRMATION,
            "ZAPI_INSTANCE_ID": "i",
            "ZAPI_TOKEN": "t",
            "ZAPI_CLIENT_TOKEN": "c",
        }
        with patch.dict(os.environ, environment, clear=True):
            main.main()

        send_text_message.assert_called_once()
        mark_delivered.assert_called_once()
        self.assertEqual(mark_delivered.call_args.kwargs["phone"], "5521999990000")


if __name__ == "__main__":
    unittest.main()