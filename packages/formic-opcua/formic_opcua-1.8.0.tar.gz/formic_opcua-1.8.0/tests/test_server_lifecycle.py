# Copyright Formic Technologies 2024
import unittest
from unittest.mock import AsyncMock

from formic_opcua import OpcuaServer


class TestOpcuaServerLifecycle(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_config_filename = 'data/ok_server_config.yaml'

    def setUp(self):
        self.server = OpcuaServer(self.server_config_filename)
        self.server._server = AsyncMock()

    async def test_configure(self):
        await self.server.configure()
        self.assertTrue(self.server._server.init.called)
        self.assertTrue(self.server._server.set_endpoint.called)
        self.assertTrue(self.server._server.set_server_name.called)
        self.assertTrue(self.server._server.set_security_policy.called)
        self.assertTrue(self.server._server.set_security_IDs.called)
        self.server._server.set_endpoint.assert_called_with(url='opc.tcp://localhost:4840/COMPANY_NAME/opcua/')
        self.server._server.set_server_name.assert_called_with(name='COMPANY_NAME')

    async def test_run(self):
        await self.server.run()
        self.assertTrue(self.server._server.start.called)
        self.assertEqual(len(self.server.objects), 9)

    async def test_stop(self):
        await self.server.stop()
        self.assertTrue(self.server._server.stop.called)

    async def test_launch(self):
        await self.server.launch()
        self.assertTrue(self.server._server.init.called)
        self.assertTrue(self.server._server.set_endpoint.called)
        self.assertTrue(self.server._server.start.called)


if __name__ == '__main__':
    unittest.main()
