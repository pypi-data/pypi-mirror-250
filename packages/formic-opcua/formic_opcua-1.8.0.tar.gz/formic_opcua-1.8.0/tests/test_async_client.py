import asyncio
import unittest
from unittest.mock import patch

import asyncua
from asyncua import Client, Node
from asyncua.common.subscription import Subscription
from asyncua.ua.uatypes import DataValue

from formic_opcua import AsyncOpcuaClient, ConnectionStatus, OpcuaServer, SubHandler


class TestAsyncOpcuaClient(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.ok_node_path = '/formic/device_type/PLC/device/SYS1_PLC1/states/system_state'
        cls.nok_node_path = 'bad_path'
        cls.ok_server_config_path = 'data/ok_server_config.yaml'

    async def asyncSetUp(self):
        self.server = OpcuaServer(self.ok_server_config_path)
        await self.server.launch()

    async def asyncTearDown(self):
        await self.server.stop()

    async def test_connect(self):
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertEqual(client.connection_status, ConnectionStatus.CONNECTED)

    async def test_disconnect(self):
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            pass
        self.assertEqual(client.connection_status, ConnectionStatus.TERMINATE)

    async def test_dfs_mapper(self):
        expected_node_paths = [
            '/formic/device_type/PLC/device/SYS1_PLC1/connection/connection_status',
            '/formic/device_type/PLC/device/SYS1_PLC1/states/system_safety_status',
            '/formic/device_type/PLC/device/SYS1_PLC1/states/system_state',
            '/formic/device_type/PLC/device/SYS1_PLC1/states/critical_system_statuses/level_1_errors',
            '/formic/device_type/PLC/device/SYS1_PLC1/states/critical_system_statuses/level_2_errors',
        ]
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertEqual(list(client._node_map.keys()), expected_node_paths)

    async def test_read_ok(self):
        expected_value = 0

        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertEqual(await client.read(self.ok_node_path), expected_value)

    async def test_write_ok(self):
        expected_value_before_write = 0
        expected_value_after_write = 1

        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertEqual(await client.read(self.ok_node_path), expected_value_before_write)
            self.assertTrue(await client.write(self.ok_node_path, expected_value_after_write))
            self.assertEqual(await client.read(self.ok_node_path), expected_value_after_write)

    @patch.object(Node, 'read_value')
    async def test_read_timeout_error(self, patch_read_value):
        patch_read_value.side_effect = asyncio.TimeoutError
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertIsNone(await client.read(self.ok_node_path))

    @patch.object(Node, 'write_value')
    async def test_write_timeout_error(self, patch_write_value):
        async def raise_async_timeout(datavalue):
            #  asyncua uses Node.write_value internally to update server timestamp,
            #  only attempt to write DataValue should raise exception
            if isinstance(datavalue, DataValue):
                raise asyncio.TimeoutError

        patch_write_value.side_effect = raise_async_timeout

        expected_value_before_after_write = 0
        value_to_write = 1

        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertEqual(await client.read(self.ok_node_path), expected_value_before_after_write)
            self.assertFalse(await client.write(self.ok_node_path, value_to_write))
            self.assertEqual(await client.read(self.ok_node_path), expected_value_before_after_write)

    async def test_read_bad_path(self):
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertIsNone(await client.read(self.nok_node_path))

    async def test_write_bad_path(self):
        path = 'bad_path'
        value_to_write = 0
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertFalse(await client.write(path, value_to_write))

    async def test_subscription_creation(self):
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            await client.subscribe_all()
            #  Wait for subscription handler reaction
            await asyncio.sleep(1)
            self.assertIsInstance(client.sub_handler, SubHandler)
            self.assertIsInstance(client._sub, Subscription)

    async def test_read_from_subscription(self):
        expected_value_before_write = 0
        expected_value_after_write = 1
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            await client.subscribe_all()
            #  Wait for subscription handler reaction
            await asyncio.sleep(1)
            all_values = await client.read_all_from_subscription()
            self.assertEqual(all_values[self.ok_node_path], expected_value_before_write)
            self.assertTrue(await client.write(self.ok_node_path, expected_value_after_write))
            #  Wait for subscription handler reaction
            await asyncio.sleep(1)
            all_values = await client.read_all_from_subscription()
            self.assertEqual(all_values[self.ok_node_path], expected_value_after_write)

    async def test_read_from_subscription_before_subscription(self):
        expected_response = {}
        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            self.assertEqual(await client.read_all_from_subscription(), expected_response)

    @patch.object(AsyncOpcuaClient, '_establish_server_structure')
    @patch.object(AsyncOpcuaClient, '_test_server_connection')
    @patch.object(Client, 'disconnect')
    @patch.object(Client, 'connect')
    async def test_failed_connection_test_dev(
        self, patch_client_connect, patch_client_disconnect, patch_check_connection, _
    ):
        patch_client_connect.return_value = True
        patch_client_disconnect.return_value = True
        patch_check_connection.return_value = True

        async with AsyncOpcuaClient(self.ok_server_config_path) as client:
            client._client = asyncua.Client(url='')
            patch_check_connection.return_value = False
            await asyncio.sleep(3)
            patch_check_connection.return_value = True
            while client.connection_status != ConnectionStatus.CONNECTED:
                await asyncio.sleep(1)
            #  There must be at least one connection attempt, not including context manager enter
            self.assertGreaterEqual(patch_client_connect.call_count, 2)
            #  There must be at least one disconnection (reconnection) attempt
            self.assertGreaterEqual(patch_client_disconnect.call_count, 1)


if __name__ == '__main__':
    unittest.main()
