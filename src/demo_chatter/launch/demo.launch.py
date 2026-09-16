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

"""Lanza talker y listener juntos, con parametros configurables."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Construye la descripcion de lanzamiento de la demo."""
    mensaje = LaunchConfiguration('mensaje')
    periodo = LaunchConfiguration('periodo_s')

    return LaunchDescription([
        DeclareLaunchArgument('mensaje', default_value='hola equipo'),
        DeclareLaunchArgument('periodo_s', default_value='1.0'),
        Node(
            package='demo_chatter',
            executable='talker',
            name='talker',
            output='screen',
            parameters=[{'mensaje': mensaje, 'periodo_s': periodo}],
        ),
        Node(
            package='demo_chatter',
            executable='listener',
            name='listener',
            output='screen',
        ),
    ])
