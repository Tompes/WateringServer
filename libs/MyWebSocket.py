from tornado.websocket import WebSocketHandler


class WebSocket(WebSocketHandler):
    pool = set()
    name = "default"

    def accept_connection(self):
        try:
            self._handle_websocket_headers()
        except ValueError:
            self.handler.set_status(400)
            log_msg = "Missing/Invalid WebSocket headers"
            self.handler.finish(log_msg)
            return

        try:
            self._accept_connection()
        except ValueError:

            self._abort()
            return

    def check_origin(self, origin):
        return True

    def open(self):
        try:
            self.set_nodelay(True)
        except:
            pass
        self.clean_dead()
        WebSocket.pool.add(self)

        print("Socket opened. now:" + str(len(WebSocket.pool)))

    def close(self):
        if self.name == 'terminal':
            for i in WebSocket.pool:
                if i.name == 'user':
                    i.write_message('terminal_offline')
        WebSocket.pool.remove(self)
        self.clean_dead()
        print("Socket closed. now:" + str(len(WebSocket.pool)))

    def on_ping(self, data: bytes) -> None:
        print("ping:" + self.name)

    def on_pong(self, data: bytes) -> None:
        print("pong:" + self.name)

    def on_message(self, message):
        self.clean_dead()

        self.write_message("Received: " + message)
        if self.name == 'terminal':
            for i in WebSocket.pool:
                if i.name == 'user':
                    i.write_message(message)
        print("Received message: " + message)
        if message == 'user':
            self.name = 'user'
            self.write_message("hello!")
        if message == 'terminal_status':
            t = 0
            for i in WebSocket.pool:
                if i.name == 'terminal':
                    t = 1
                    break
            if t == 0:
                self.write_message('terminal_offline')
            else:
                self.write_message('terminal_online')

        if message == 'terminal':
            self.name = 'terminal'
            for i in WebSocket.pool:
                if i.name == 'user':
                    i.write_message('terminal_online')
        if message == 'autoWatering':
            for i in WebSocket.pool:
                i.write_message('auto_watering')
        if message == 'turnLEDOn':
            for i in WebSocket.pool:
                if i.name == "terminal":
                    i.write_message('turn_led_on')
        if message == 'turnLEDOff':
            for i in WebSocket.pool:
                if i.name == "terminal":
                    i.write_message('turn_led_off')
        if message == 'turnOnMotorRight':
            for i in WebSocket.pool:
                i.write_message('motor_right')
        if message == 'turnOnMotorLeft':
            for i in WebSocket.pool:
                i.write_message('motor_left')
        if message == 'turnMotorOff':
            for i in WebSocket.pool:
                i.write_message('turn_motor_off')

    def clean_dead(self):
        print("Clean dead connections...")
        for i in WebSocket.pool.copy():  # 移除死亡Client
            try:
                i.ping()
            except:
                print("REMOVE")
                WebSocket.pool.remove(i)
    # def getOnline(self):
    #     return self.pool;
