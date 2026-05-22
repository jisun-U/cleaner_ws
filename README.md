# LLM based cleaning robot

프로젝트 목적 : 사용자의 맥락적 요구사항(Contextual Requirements) 분석을 통한 지능형 시설 관리 인터페이스 구현




isaacsim 환경 실행
```
source /opt/ros/humble/setup.bash
conda activate {가상환경 이름}
~/isaac-sim/python.sh {directory}/cleaner_ws/cleaner_IsaacSim/Main/main.py
```


### slam mode

teleop 명령으로 로봇 이동하며 맵 작성

```
ros2 launch slam_toolbox online_async_launch.py \
    slam_params_file:={directory}/cleaner_ws/phyAI_ws/slam_toolbox_params.yaml \
    use_sim_time:=true
```

### nav2_bringup mode
```
ros2 launch nav2_bringup bringup_launch.py \
use_sim_time:=true \
map:={directory}/cleaner_ws/phyAI_ws/map/may15_v2_revised.yaml \
params_file:={directory}/cleaner_ws/phyAI_ws/nav2_localization_params.yaml
```


rviz에서 2D Nav Goal지정 후, map 그리기


### 디렉토리 구조
```
cleaner_ws/
├── cleaner_IsaacSim/                     
│   ├── Main/                               
│   │   ├── app/   
│   │   │    ├── graph_builder.py
│   │   │    ├── loop.py
│   │   │    ├── utils.py  
│   │   │    └── world.py                          
│   │   ├── configs/  
│   │   │       └── default.yaml     
│   │   └── main.py                         # isaacsim simulation executable file                    
│   │
│   ├── cleaner_Mechanics/                 
│   │   ├── urdf/                           
│   │   ├── usd_file/                       
│   │   └── meshes/                         
│
├── phy_ws/                                 # 실제 로봇 하드웨어 제어(node)
│   ├── src/                                # 개발중(완료x)
│   │   ├── cleaner_system1/               
│   │   ├── cleaner_system2/               
│   │   ├── gptapi/             
│   │   ├── usb_cam/             
│   │   └── yolov8_ros/             
│   │
│   ├── config/       
│   │     ├── nav2_params.yaml
│   │     ├── nav2_slam_only.yaml 
│   │     └── slam_toolbox_params.yaml                                         
│   └── tmuxp_slam_mode.yaml                     
│                          
└── README.md                              
```

  
