from pxr import Sdf
from omni.isaac.core.utils.extensions import enable_extension


class GraphBuilder:
    """
    Isaac Sim <-> ROS 2 브릿지용 OmniGraph를 구성합니다.
      - 카메라 RGB/CameraInfo 퍼블리시
      - Spot 제어(vel/joint), JointState 퍼블리시
      - Clock / IMU / Odometry / TF 트리 퍼블리시
      - RTX LiDAR(2D/3D) LaserScan/PointCloud 퍼블리시
    """
    def __init__(self, assets_cfg: dict, ros_cfg: dict):
        import omni.usd
        import omni.timeline
        

        self.assets = assets_cfg
        self.ros = ros_cfg

        # 타임라인 재생
        self.timeline = omni.timeline.get_timeline_interface()
        self.timeline.play()

        # 스테이지 핸들
        self.stage = omni.usd.get_context().get_stage()

        # 필요한 익스텐션 활성화
        for ext in [
            "omni.anim.people",
            "omni.anim.graph.bundle",
            "omni.kit.scripting",
            "omni.anim.graph.ui",
            "omni.anim.graph.schema",
            "omni.anim.navigation.schema",
            "omni.graph.action_nodes",
            "omni.graph.nodes",
            "isaacsim.core.nodes",
            "isaacsim.ros2.bridge",
            "omni.isaac.sensor",           # RTX LiDAR
            "isaacsim.robot.wheeled_robots",
        ]:
            try:
                enable_extension(ext)
            except Exception:
                # 없는 경우도 있으므로 무시
                pass

        # 캐릭터/애니메이션용 루트 (기존 코드 호환용)
        self._define_character_graph_roots()

    # --------------------------------------------------------------------- #
    # 내부 유틸
    # --------------------------------------------------------------------- #
    def _define_character_graph_roots(self):
        from omni.isaac.core.utils.prims import define_prim
        define_prim("/World/CustomGraph", "Xform")
        define_prim("/World/CustomGraph/CharacterAnimation", "Xform") 
        define_prim("/World/CustomGraph/CharacterAnimation/AnimationGraph", "AnimationGraph")

    # --------------------------------------------------------------------- #
    # 카메라 ROS 퍼블리셔 그래프
    # --------------------------------------------------------------------- #
    def build_camera_ros_graph(self, graph_path: str = "/CameraActionGraph"):
        import omni.graph.core as og
        keys = og.Controller.Keys
        
        CAMERA_PRIM = Sdf.Path(self.assets["camera_prim"])

        (graph, _, _, _) = og.Controller.edit(
            {
                "graph_path": graph_path,
                "evaluator_name": "execution", # push 대신 execution 사용
                # pipeline_stage를 제거하거나 SIMULATION으로 변경
            },
            {
                keys.CREATE_NODES: [
                    ("OnTick", "omni.graph.action.OnTick"),
                    # Viewport 대신 직접 RenderProduct 생성 (Lidar와 동일한 방식)
                    ("createRenderProduct", "isaacsim.core.nodes.IsaacCreateRenderProduct"),
                    ("cameraHelperRgb", "isaacsim.ros2.bridge.ROS2CameraHelper"),
                    ("cameraHelperInfo", "isaacsim.ros2.bridge.ROS2CameraInfoHelper"),
                    ("cameraHelperDepth", "isaacsim.ros2.bridge.ROS2CameraHelper"),
                ],

                keys.CONNECT: [
                    ("OnTick.outputs:tick", "createRenderProduct.inputs:execIn"),
                    ("createRenderProduct.outputs:execOut", "cameraHelperRgb.inputs:execIn"),
                    ("createRenderProduct.outputs:execOut", "cameraHelperInfo.inputs:execIn"),
                    ("createRenderProduct.outputs:execOut", "cameraHelperDepth.inputs:execIn"),

                    ("createRenderProduct.outputs:renderProductPath", "cameraHelperRgb.inputs:renderProductPath"),
                    ("createRenderProduct.outputs:renderProductPath", "cameraHelperInfo.inputs:renderProductPath"),
                    ("createRenderProduct.outputs:renderProductPath", "cameraHelperDepth.inputs:renderProductPath"),
                ],

                keys.SET_VALUES: [
                    ("createRenderProduct.inputs:cameraPrim", CAMERA_PRIM), # 리스트 대신 경로 직접 전달
                    ("createRenderProduct.inputs:width", 640),
                    ("createRenderProduct.inputs:height", 480),

                    # RGB 설정
                    ("cameraHelperRgb.inputs:frameId", self.ros["frames"]["camera_frame"]),
                    ("cameraHelperRgb.inputs:topicName", self.ros["topics"]["camera_rgb"]),
                    ("cameraHelperRgb.inputs:type", "rgb"),

                    # Info 설정
                    ("cameraHelperInfo.inputs:frameId", self.ros["frames"]["camera_frame"]),
                    ("cameraHelperInfo.inputs:topicName", self.ros["topics"]["camera_info"]),

                    # Depth 설정
                    ("cameraHelperDepth.inputs:frameId", self.ros["frames"]["camera_frame"]),
                    ("cameraHelperDepth.inputs:topicName", self.ros["topics"]["camera_depth"]),
                    ("cameraHelperDepth.inputs:type", "depth"),
            ],
        },
    )
        og.Controller.evaluate_sync(graph)
    # --------------------------------------------------------------------- #
    # Spot/ATS + 시계/IMU/Odom/TF 그래프
    # --------------------------------------------------------------------- #
    def build_backbon_graph(self, graph_path: str = "/BackbonActionGraph"):
        """
        - ROS2Context
        - Spot 제어:
            * Twist 구독(vel), JointState 명령 구독
            * JointState 퍼블리시
        - Clock 퍼블리시
        - IMU 퍼블리시(시뮬 가속/각속/자세)
        - Odometry 퍼블리시(odom -> base_link)
        - TF 퍼블리시: 카메라/IMU(base_link 자식), odom 트리(odom -> base_link)
        """
        import omni.graph.core as og
        keys = og.Controller.Keys

        ROBOT_PRIM = Sdf.Path(self.assets.get("cleaner_prim", self.assets["base_link"]))
        BASE_PRIM = Sdf.Path(self.assets["base_link"])
        CAMERA_PRIM    = Sdf.Path(self.assets["camera_prim"])
        IMU_PRIM = Sdf.Path(self.assets["imu_prim"])
        ODOM_PRIM      = Sdf.Path(self.assets["odom_prim"])   # 프레임 "odom"과 연결
        jointNames = ["left_wheel_joint", "right_wheel_joint"]
        LEFT_DROP_PRIM = Sdf.Path(self.assets["wheel_drop_left_prim"])
        RIGHT_DROP_PRIM = Sdf.Path(self.assets["wheel_drop_right_prim"])
        LEFT_PRIM      = Sdf.Path(self.assets["left_wheel_prim"])
        RIGHT_PRIM      = Sdf.Path(self.assets["right_wheel_prim"])
        DOMAIN_ID= self.ros["domain_id"]

        if not self.stage.GetPrimAtPath(str(ODOM_PRIM)).IsValid():
            from omni.isaac.core.utils.prims import define_prim
            define_prim(str(ODOM_PRIM), "Xform")

        (graph, _, _, _) = og.Controller.edit(
            {"graph_path": graph_path, "evaluator_name": "execution"},
            {
                keys.CREATE_NODES: [
                    # ROS2 컨텍스트
                    ("Context",        "isaacsim.ros2.bridge.ROS2Context"),
                    # simulation time
                    ("SimulationTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),



                    # 초기 1회 트리거 
                    ("OnImpulseEvent", "omni.graph.action.OnImpulseEvent"),

                    # 제어/상태
                    ("SubscribeTwist",          "isaacsim.ros2.bridge.ROS2SubscribeTwist"), 
                    ("PublishJointState",   "isaacsim.ros2.bridge.ROS2PublishJointState"),  
                    ("ArticulationController",  "isaacsim.core.nodes.IsaacArticulationController"), 
                    ("DifferentialController", "isaacsim.robot.wheeled_robots.DifferentialController"), # subscribe twist → diff ctrl → articulation ctrl 흐름용

                    ("AngularBreak3Vector", "omni.graph.nodes.BreakVector3"),
                    ("LinearBreak3Vector", "omni.graph.nodes.BreakVector3"),

                    ("TFPubRightDrop",      "isaacsim.ros2.bridge.ROS2PublishTransformTree"),
                    ("TFPubLeftDrop",       "isaacsim.ros2.bridge.ROS2PublishTransformTree"),
                    ("TFPubRightWheel",     "isaacsim.ros2.bridge.ROS2PublishTransformTree"),
                    ("TFPubLeftWheel",      "isaacsim.ros2.bridge.ROS2PublishTransformTree"),



                    # 매 프레임 트리거 > odom, tf publisher는 Tick, IMU 퍼블리셔는 OnTickIMU로 분리하여 제어
                    ("Tick",           "omni.graph.action.OnPlaybackTick"),

                    # Clock
                    ("ClockPub",  "isaacsim.ros2.bridge.ROS2PublishClock"), 

                    # IMU
                    ("OnTickIMU",       "omni.graph.action.OnTick"),
                    ("ImuComputeOdom",  "isaacsim.core.nodes.IsaacComputeOdometry"),
                    ("ImuPublish",      "isaacsim.ros2.bridge.ROS2PublishImu"),

                    # Odom
                    ("OdomCompute", "isaacsim.core.nodes.IsaacComputeOdometry"),
                    ("OdomPublish", "isaacsim.ros2.bridge.ROS2PublishOdometry"),

                    # TF (cam/imu)
                    ("TFPubCam",          "isaacsim.ros2.bridge.ROS2PublishTransformTree"),
                    ("TFPubImu",          "isaacsim.ros2.bridge.ROS2PublishTransformTree"),

                    # TF (odom) - 별도 노드로 분리하여 시뮬레이션 시간과 트랜스폼 갱신 타이밍을 odom과 맞춤
                    ("TFPubOdom",       "isaacsim.ros2.bridge.ROS2PublishTransformTree"),
                ],
                keys.CONNECT: [
                    # 제어/상태

                    # 매 프레임 ROS 입력 처리/상태 퍼블리시/제어 적용
                    ("Tick.outputs:tick", "SubscribeTwist.inputs:execIn"),
                    ("Tick.outputs:tick", "PublishJointState.inputs:execIn"),
                    ("Tick.outputs:tick", "ArticulationController.inputs:execIn"),
                    #매세지 올 때마다 트리거
                    ("SubscribeTwist.outputs:execOut","DifferentialController.inputs:execIn"),
                    # 컨텍스트 연결
                    ("Context.outputs:context", "SubscribeTwist.inputs:context"),
                    ("Context.outputs:context", "PublishJointState.inputs:context"),
                    ("SimulationTime.outputs:simulationTime","PublishJointState.inputs:timeStamp"),
                    # Twist → Diff Ctrl → Articulation Ctrl 흐름
                    ("SubscribeTwist.outputs:linearVelocity", "LinearBreak3Vector.inputs:tuple"),
                    ("SubscribeTwist.outputs:angularVelocity", "AngularBreak3Vector.inputs:tuple"),
                    ("LinearBreak3Vector.outputs:x", "DifferentialController.inputs:linearVelocity"),
                    ("AngularBreak3Vector.outputs:z", "DifferentialController.inputs:angularVelocity"),
                    ("Tick.outputs:deltaSeconds", "DifferentialController.inputs:dt"),
                    ("DifferentialController.outputs:velocityCommand", "ArticulationController.inputs:velocityCommand"),

                    ("Context.outputs:context", "ClockPub.inputs:context"),
                    ("SimulationTime.outputs:simulationTime", "ClockPub.inputs:timeStamp"),
                    ("Tick.outputs:tick", "ClockPub.inputs:execIn"),

                    # IMU(매 프레임)
                    ("OnTickIMU.outputs:tick", "ImuComputeOdom.inputs:execIn"),
                    ("OnTickIMU.outputs:tick", "ImuPublish.inputs:execIn"),
                    ("Context.outputs:context", "ImuPublish.inputs:context"),
                    ("ImuComputeOdom.outputs:orientation",        "ImuPublish.inputs:orientation"),
                    ("ImuComputeOdom.outputs:angularVelocity",    "ImuPublish.inputs:angularVelocity"),
                    ("ImuComputeOdom.outputs:linearAcceleration", "ImuPublish.inputs:linearAcceleration"),
                    ("SimulationTime.outputs:simulationTime",     "ImuPublish.inputs:timeStamp"),

                    # Odom(매 프레임)
                    ("Tick.outputs:tick", "OdomCompute.inputs:execIn"),
                    ("Tick.outputs:tick", "OdomPublish.inputs:execIn"),
                    ("Context.outputs:context", "OdomPublish.inputs:context"),
                    ("OdomCompute.outputs:position",        "OdomPublish.inputs:position"),
                    ("OdomCompute.outputs:orientation",     "OdomPublish.inputs:orientation"),
                    ("OdomCompute.outputs:linearVelocity",  "OdomPublish.inputs:linearVelocity"),
                    ("OdomCompute.outputs:angularVelocity", "OdomPublish.inputs:angularVelocity"),
                    ("SimulationTime.outputs:simulationTime", "OdomPublish.inputs:timeStamp"),

                    # TF(cam/imu/odom)
                    ("Tick.outputs:tick", "TFPubCam.inputs:execIn"),
                    ("Tick.outputs:tick", "TFPubImu.inputs:execIn"),
                    ("Tick.outputs:tick", "TFPubOdom.inputs:execIn"),
                    ("Tick.outputs:tick", "TFPubRightDrop.inputs:execIn"),
                    ("Tick.outputs:tick", "TFPubLeftDrop.inputs:execIn"),
                    ("Tick.outputs:tick", "TFPubRightWheel.inputs:execIn"),
                    ("Tick.outputs:tick", "TFPubLeftWheel.inputs:execIn"),
                    ("Context.outputs:context", "TFPubCam.inputs:context"),
                    ("Context.outputs:context", "TFPubImu.inputs:context"),
                    ("Context.outputs:context", "TFPubOdom.inputs:context"),
                    ("Context.outputs:context", "TFPubRightDrop.inputs:context"),
                    ("Context.outputs:context", "TFPubLeftDrop.inputs:context"),
                    ("Context.outputs:context", "TFPubRightWheel.inputs:context"),
                    ("Context.outputs:context", "TFPubLeftWheel.inputs:context"),
                    ("SimulationTime.outputs:simulationTime", "TFPubCam.inputs:timeStamp"),
                    ("SimulationTime.outputs:simulationTime", "TFPubImu.inputs:timeStamp"),
                    ("SimulationTime.outputs:simulationTime",   "TFPubOdom.inputs:timeStamp"),
                    ("SimulationTime.outputs:simulationTime", "TFPubRightDrop.inputs:timeStamp"),
                    ("SimulationTime.outputs:simulationTime", "TFPubLeftDrop.inputs:timeStamp"),
                    ("SimulationTime.outputs:simulationTime", "TFPubRightWheel.inputs:timeStamp"),
                    ("SimulationTime.outputs:simulationTime", "TFPubLeftWheel.inputs:timeStamp"),


                ],
                keys.SET_VALUES: [

                    ("Context.inputs:domain_id",DOMAIN_ID), 
                    # 제어 타깃(cleaner)
                    ("ArticulationController.inputs:targetPrim", [ROBOT_PRIM]),
                    ("SubscribeTwist.inputs:topicName", self.ros["topics"]["cmd_twist"]),
                    ("PublishJointState.inputs:topicName", self.ros["topics"]["joint_state"]),
                    ("PublishJointState.inputs:targetPrim", [ROBOT_PRIM]),

                    ("DifferentialController.inputs:maxAngularSpeed",1.9),
                    ("DifferentialController.inputs:maxLinearSpeed",0.31),
                    ("DifferentialController.inputs:wheelDistance",0.235),
                    ("DifferentialController.inputs:wheelRadius",0.033),
                    ("ArticulationController.inputs:jointNames",jointNames),

                    # IMU
                    ("ImuComputeOdom.inputs:chassisPrim", [BASE_PRIM]),
                    ("ImuPublish.inputs:frameId", self.ros["frames"]["imu_frame"]),
                    ("ImuPublish.inputs:topicName", self.ros["topics"]["imu"]),
                    ("ImuPublish.inputs:publishOrientation", True),
                    ("ImuPublish.inputs:publishAngularVelocity", True),
                    ("ImuPublish.inputs:publishLinearAcceleration", True),
                    ("OnTickIMU.inputs:framePeriod", 0),
                    ("OnTickIMU.inputs:onlyPlayback", True),

                    #clock
                    ("ClockPub.inputs:topicName", self.ros["topics"]["clock"]),
                    ("ClockPub.inputs:queueSize", 10), # 기본 10으로 했을때 에러 생성

                    # Odom (odom -> base_link)
                    ("OdomCompute.inputs:chassisPrim", [BASE_PRIM]),
                    ("OdomPublish.inputs:topicName", self.ros["topics"]["odom"]),
                    ("OdomPublish.inputs:odomFrameId", self.ros["frames"]["odom"]),
                    ("OdomPublish.inputs:chassisFrameId", self.ros["frames"]["base_link"]),

                    # TF - Cam / IMU (부모: base_link)
                    ("TFPubCam.inputs:parentPrim", [BASE_PRIM]),
                    ("TFPubCam.inputs:targetPrims", [CAMERA_PRIM]),
                    ("TFPubImu.inputs:parentPrim", [BASE_PRIM]),
                    ("TFPubImu.inputs:targetPrims", [IMU_PRIM]),

                    # TF - Odom 트리 (부모: /World/odom, 자식: base_link)
                    ("TFPubOdom.inputs:parentPrim", [ODOM_PRIM]),
                    ("TFPubOdom.inputs:targetPrims", [BASE_PRIM]),

                    # TF - wheel chain
                    ("TFPubLeftDrop.inputs:parentPrim", [BASE_PRIM]),
                    ("TFPubLeftDrop.inputs:targetPrims", [LEFT_DROP_PRIM]),
                    ("TFPubLeftWheel.inputs:parentPrim", [LEFT_DROP_PRIM]),
                    ("TFPubLeftWheel.inputs:targetPrims", [LEFT_PRIM]),
                    ("TFPubRightDrop.inputs:parentPrim", [BASE_PRIM]),
                    ("TFPubRightDrop.inputs:targetPrims", [RIGHT_DROP_PRIM]),
                    ("TFPubRightWheel.inputs:parentPrim", [RIGHT_DROP_PRIM]),
                    ("TFPubRightWheel.inputs:targetPrims", [RIGHT_PRIM]),
                ],
            },
        )
        og.Controller.evaluate_sync(graph)

    # --------------------------------------------------------------------- #
    # RTX LiDAR (2D) ROS 퍼블리셔 그래프
    # --------------------------------------------------------------------- #
  
    def build_lidar_ros_graph(self, full_cfg: dict, graph_path: str = "/LidarGraph"):
        """
        Isaac Sim 5.0 기준
        - 2D: ROS2RtxLidarHelper(type="laser_scan")  -> topics["scan"]
        - 3D: ROS2RtxLidarHelper(type="point_cloud")-> topics["point_cloud"]
        - 각 LiDAR prim을 RenderProduct.cameraPrim으로 직접 사용
        - TF(부모=base_link, 자식=각 LiDAR prim)
        """
        import omni.graph.core as og
        from pxr import UsdGeom, Sdf

        keys = og.Controller.Keys

        LIDAR_PRIM_2D = Sdf.Path(self.assets["lidar_prim_2d"])# e.g., {"create_2d": True, "prim_2d": "/World/Spot/Lidar2D", ...}
        BASE_LINK= Sdf.Path(self.assets["base_link"])
        DOMAIN_ID= self.ros["domain_id"]
        
        create_nodes = [
            ("Tick", "omni.graph.action.OnPlaybackTick"),
            ("RunSim", "isaacsim.core.nodes.OgnIsaacRunOneSimulationFrame"),
            ("Ctx", "isaacsim.ros2.bridge.ROS2Context"),

            ("RP_2D", "isaacsim.core.nodes.IsaacCreateRenderProduct"), #렌더 프러덕트
            ("TFTime2D", "isaacsim.core.nodes.IsaacReadSimulationTime"), 
            ("TFLidar2D", "isaacsim.ros2.bridge.ROS2PublishTransformTree"), #tf publish
            ("Lidar2D", "isaacsim.ros2.bridge.ROS2RtxLidarHelper"), #헬퍼
        ]

        connect = [
            ("Tick.outputs:tick", "RunSim.inputs:execIn"),

            ("RunSim.outputs:step", "RP_2D.inputs:execIn"),
            ("RP_2D.outputs:renderProductPath", "Lidar2D.inputs:renderProductPath"),
            ("RP_2D.outputs:execOut", "Lidar2D.inputs:execIn"),
            ("Ctx.outputs:context", "Lidar2D.inputs:context"),

            ("Tick.outputs:tick", "TFLidar2D.inputs:execIn"),
            ("Ctx.outputs:context", "TFLidar2D.inputs:context"),
            ("TFTime2D.outputs:simulationTime", "TFLidar2D.inputs:timeStamp"),
        ]

        setvals = [
            ("Ctx.inputs:domain_id", DOMAIN_ID),

            ("RP_2D.inputs:enabled", True),
            ("RP_2D.inputs:cameraPrim", [str(LIDAR_PRIM_2D)]),
            ("RP_2D.inputs:width", 640),
            ("RP_2D.inputs:height", 1), #320 > 1로 변경 (2D LiDAR는 1라인이므로)

            ("Lidar2D.inputs:enabled", True),
            ("Lidar2D.inputs:type", "laser_scan"),
            ("Lidar2D.inputs:topicName", self.ros["topics"]["scan"]),
            ("Lidar2D.inputs:frameId", self.ros["frames"]["base_scan"]),
            ("Lidar2D.inputs:frameSkipCount", 0),
            ("Lidar2D.inputs:nodeNamespace", ""),

            ("TFLidar2D.inputs:parentPrim", [str(BASE_LINK)]),
            ("TFLidar2D.inputs:targetPrims", [str(LIDAR_PRIM_2D)]),
        ]



        # 그래프 생성/적용
        (graph, _, _, _) = og.Controller.edit(
            {"graph_path": graph_path, "evaluator_name": "execution"},
            {keys.CREATE_NODES: create_nodes, keys.CONNECT: connect, keys.SET_VALUES: setvals},
        )
        # 즉시 계산(그래프 활성화)
        og.Controller.evaluate_sync(graph)
