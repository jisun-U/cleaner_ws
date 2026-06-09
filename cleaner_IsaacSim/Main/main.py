from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": True})
simulation_app.update()

from isaacsim.core.utils.extensions import enable_extension

enable_extension("isaacsim.ros2.bridge")
enable_extension("isaacsim.robot.wheeled_robots")
enable_extension("isaacsim.core.nodes")
enable_extension("omni.graph.action_nodes")
enable_extension("omni.graph.nodes")
simulation_app.update()

from app.graph_builder import GraphBuilder
from app.loop import SimLoop
from app.utils import load_cfg
from app.world import SimWorld

cfg = load_cfg()

world = SimWorld(
    usd_path=cfg["assets"]["usd_path"],
    cleaner_prim=cfg["assets"]["cleaner_prim"],
    articulation_root=cfg["assets"]["base_link"],
    semantic_labels=cfg["assets"].get("semantic_labels", []),
    imu_dummy_prim="",
    fixed_time_step=True,
    play_every_frame=True,
    target_hz=60,
)
simulation_app.update()

graph_builder = GraphBuilder(cfg["assets"], cfg["ros"])
graph_builder.build_backbon_graph()
graph_builder.build_camera_ros_graph()
graph_builder.build_lidar_ros_graph(cfg)

try:
    loop = SimLoop(simulation_app, world, render=True)
    loop.run()
finally:
    simulation_app.close()
