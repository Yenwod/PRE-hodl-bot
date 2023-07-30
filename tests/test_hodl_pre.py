import unittest
import os
import asyncio
from datetime import datetime
from unittest.mock import MagicMock, patch
from hodl_pre import get_last_execution_time, set_last_execution_time, is_same_day, send_telegram_message, main


class TestHodlPre(unittest.IsolatedAsyncioTestCase):
    @patch("builtins.open")
    def test_get_last_execution_time(self, mock_open):
        mock_file = MagicMock()
        mock_file.read.return_value = "2022-01-01T00:00:00"
        mock_open.return_value.__enter__.return_value = mock_file

        last_execution_time = get_last_execution_time()

        self.assertEqual(last_execution_time.year, 2022)
        self.assertEqual(last_execution_time.month, 1)
        self.assertEqual(last_execution_time.day, 1)
        self.assertEqual(last_execution_time.hour, 0)
        self.assertEqual(last_execution_time.minute, 0)
        self.assertEqual(last_execution_time.second, 0)

    @patch("builtins.open")
    def test_set_last_execution_time(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        set_last_execution_time(datetime(2022, 1, 1, 0, 0, 0))

        mock_file.write.assert_called_once_with("2022-01-01T00:00:00")

    def test_is_same_day(self):
        date1 = datetime(2022, 1, 1, 0, 0, 0)
        date2 = datetime(2022, 1, 1, 12, 0, 0)
        date3 = datetime(2022, 1, 2, 0, 0, 0)

        self.assertTrue(is_same_day(date1, date2))
        self.assertFalse(is_same_day(date1, date3))

    @patch("telegram.Bot.send_message")
    async def test_send_telegram_message(self, mock_send_message):
        await send_telegram_message("test message")
        mock_send_message.assert_called_once_with(chat_id=os.getenv("chat_id"), text="test message")

    @patch("builtins.open")
    @patch("coinex.coinex.CoinEx.order_market")
    @patch("coinex.coinex.CoinEx.balance_info")
    @patch("telegram.Bot.send_message")
    def test_main_with_sufficient_balance(self, mock_send_message, mock_balance_info, mock_order_market, mock_open):
        mock_balance_info.return_value = {"USDT": {"available": 100.0}}

        # Set the mock last execution time to more than a day ago
        mock_execution_time = datetime(2022, 1, 1, 0, 0, 0)

        # Set the return value of mock_get_last_execution_time to the mock execution time
        with patch("hodl_pre.get_last_execution_time") as mock_get_last_execution_time:
            mock_get_last_execution_time.return_value = mock_execution_time

            # Create a mock file object that doesn't write to disk
            mock_file = MagicMock()
            mock_file.__enter__.return_value.write.return_value = None
            mock_open.return_value = mock_file

            asyncio.run(main())
            mock_order_market.assert_called_once_with("PREUSDT", "buy", 5.0)

            self.assertIn("Order executed", mock_send_message.call_args.kwargs['text'])

        # Set the mock execution time to right now
        mock_execution_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        with patch("hodl_pre.get_last_execution_time") as mock_get_last_execution_time:
            mock_order_market.reset_mock()
            mock_get_last_execution_time.return_value = mock_execution_time
            asyncio.run(main())
            mock_order_market.assert_not_called()
            self.assertIn("Order already executed today", mock_send_message.call_args.kwargs['text'])
