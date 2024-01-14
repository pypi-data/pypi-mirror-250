#!/usr/bin/env python
# -*- coding: utf-8 -*-

from asyncio import TimeoutError
from unittest import IsolatedAsyncioTestCase
from unittest import main
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch
from time import time

from uscpi.client import open_connection
from uscpi.client import TCP


class TestTCP(IsolatedAsyncioTestCase):
    def setUp(self):
        self.tcp = TCP("127.0.0.1", 8080)
        self.mock_reader = AsyncMock()
        self.mock_writer = AsyncMock()
        self.mock_writer.drain = AsyncMock()
        self.mock_writer.write = Mock()

    async def test_aenter(self):
        result = await self.tcp.__aenter__()
        self.assertEqual(result, self.tcp)

    async def test_aexit(self):
        self.tcp.close = Mock()
        await self.tcp.__aexit__()
        self.tcp.close.assert_awaited_once()

    async def test_open_connection(self):
        response = await open_connection(
            "127.0.0.1", 8080, 65536, None, None, None, None
        )
        self.assertIsInstance(response, tuple)
        _, writer = response
        writer.close()
        await writer.wait_closed()

    async def test_tcp_timeout(self):
        tcp = TCP("10.0.0.0", 8080, 0.1)
        with self.assertRaises(TimeoutError):
            start = time()
            await tcp.open()
        delta = time() - start
        self.assertAlmostEqual(delta, 0.1, places=1)

    @patch("uscpi.client.open_connection")
    async def test_tcp_open(self, mock_open_connection):
        mock_open_connection.return_value = self.mock_reader, self.mock_writer
        await self.tcp.open()
        mock_open_connection.assert_called_once()
        self.assertIsNotNone(self.tcp.reader)
        self.assertIsNotNone(self.tcp.writer)

    @patch("uscpi.client.open_connection")
    async def test_tcp_close(self, mock_open_connection):
        self.tcp.reader = self.mock_reader
        self.tcp.writer = self.mock_writer
        await self.tcp.close()
        self.assertIsNone(self.tcp.reader)
        self.assertIsNone(self.tcp.writer)

    @patch("uscpi.client.open_connection")
    async def test_tcp_readline(self, mock_open_connection):
        mock_open_connection.return_value = self.mock_reader, self.mock_writer
        self.mock_reader.readline.return_value = b"test\n"
        self.assertEqual(await self.tcp.readline(), b"test\n")

    @patch("uscpi.client.open_connection")
    async def test_tcp_readuntil(self, mock_open_connection):
        mock_open_connection.return_value = self.mock_reader, self.mock_writer
        self.mock_reader.readuntil.return_value = b"test\n"
        self.assertEqual(await self.tcp.readuntil(b"\n"), b"test\n")

    @patch("uscpi.client.open_connection")
    async def test_tcp_write(self, mock_open_connection):
        mock_open_connection.return_value = self.mock_reader, self.mock_writer
        await self.tcp.write(b"test\n")
        self.mock_writer.drain.assert_awaited()
        self.mock_writer.write.assert_called_with(b"test\n")

    @patch("uscpi.client.open_connection")
    async def test_tcp_write_readline(self, mock_open_connection):
        mock_open_connection.return_value = self.mock_reader, self.mock_writer
        self.mock_reader.readline.return_value = b"test\n"
        response = await self.tcp.write_readline(b"test\n")
        self.mock_writer.drain.assert_awaited()
        self.mock_writer.write.assert_called_with(b"test\n")
        self.assertEqual(response, b"test\n")


if __name__ == "__main__":
    main()
