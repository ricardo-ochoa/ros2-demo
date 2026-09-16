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

"""Nodo publicador minimo: emite un String periodico en /chatter."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    """Publica mensajes de texto numerados a frecuencia configurable."""

    def __init__(self) -> None:
        """Declara parametros, crea el publisher y arranca el timer."""
        super().__init__('talker')

        self.declare_parameter('mensaje', 'hola equipo')
        self.declare_parameter('periodo_s', 1.0)

        periodo = self.get_parameter('periodo_s').value
        self._pub = self.create_publisher(String, 'chatter', 10)
        self._timer = self.create_timer(periodo, self._on_timer)
        self._contador = 0

        self.get_logger().info(f'Talker listo · periodo={periodo}s')

    def _on_timer(self) -> None:
        msg = String()
        msg.data = f"{self.get_parameter('mensaje').value} #{self._contador}"
        self._pub.publish(msg)
        self.get_logger().info(f'Publicado: {msg.data}')
        self._contador += 1


def main(args=None) -> None:
    """Punto de entrada del ejecutable talker."""
    rclpy.init(args=args)
    node = Talker()
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
