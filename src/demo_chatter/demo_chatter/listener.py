# Copyright 2026 Ricardo Ochoa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Nodo suscriptor minimo: escucha /chatter y registra lo que llega."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    """Se suscribe a /chatter y lleva la cuenta de mensajes recibidos."""

    def __init__(self) -> None:
        """Crea la suscripcion al topico chatter."""
        super().__init__('listener')
        self._sub = self.create_subscription(String, 'chatter', self._on_msg, 10)
        self._recibidos = 0
        self.get_logger().info('Listener suscrito a /chatter')

    def _on_msg(self, msg: String) -> None:
        self._recibidos += 1
        self.get_logger().info(f'Recibido ({self._recibidos}): {msg.data}')


def main(args=None) -> None:
    """Punto de entrada del ejecutable listener."""
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
