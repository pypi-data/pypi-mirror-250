from jupyter_server.services.kernels.websocket import KernelWebsocketHandler


class DQGPUWebsocketHandler(KernelWebsocketHandler):
    async def pre_get(self):
        kernel = self.kernel_manager.get_kernel(self.kernel_id)
        self.connection = self.kernel_websocket_connection_class(
            parent=kernel, websocket_handler=self, config=self.config
        )

        if self.get_argument("session_id", None):
            self.connection.session.session = self.get_argument("session_id")
        else:
            self.log.warning("No session ID specified")
        # For backwards compatibility with older versions
            # of the websocket connection, call a prepare method if found.
        if hasattr(self.connection, "prepare"):
            await self.connection.prepare()
