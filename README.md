# LLM-Based Cleaning Robot

본 프로젝트는 사용자의 맥락적 요구사항을 해석하는 LLM 기반 System-2와, 이를 실제 로봇 행동으로 실행하는 ROS 2 기반 System-1을 결합하여 지능형 시설 관리 인터페이스를 구현하는 것을 목표로 합니다.  
시뮬레이션 환경, 고수준 계획 수립, 이동 및 탐지, 그리고 최종 보고 생성까지 하나의 파이프라인으로 통합한 연구·개발용 워크스페이스입니다.

## Demo Video

프로젝트 실행 예시는 아래 영상에서 확인할 수 있습니다.

[Demo Video](./docs/demo-2026-06-09.webm)

## Execution Guide

GUI 모드로 실행하려면 `cleaner_IsaacSim/Main/main.py`에서 `headless` 옵션을 `False`로 설정한 뒤 실행합니다.

`main.py`, 전체 ROS 2 노드, `rviz2`를 함께 구동하려면 `tmuxp`를 사용할 수 있습니다. 실행 전 [cleaner_system.yaml](/home/sunny/cleaner_ws/phyAI_ws/cleaner_system.yaml)의 디렉터리 경로를 현재 환경에 맞게 수정해야 합니다.

```bash
tmuxp load {directory}/cleaner_ws/phyAI_ws/cleaner_system.yaml
```

`System-2`는 별도 터미널에서 비동기적으로 실행합니다.

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=21
source {directory}/cleaner_ws/phyAI_ws/install/setup.bash
ros2 run cleaner_system2 system2_node
```

## Directory Structure

```text
cleaner_ws/
├── cleaner_IsaacSim/
│   ├── Main/
│   │   ├── app/
│   │   │   ├── graph_builder.py
│   │   │   ├── loop.py
│   │   │   ├── utils.py
│   │   │   └── world.py
│   │   ├── configs/
│   │   │   └── default.yaml
│   │   └── main.py                     # Isaac Sim simulation entry point
│   ├── cleaner_Mechanics/
│   │   ├── urdf/
│   │   ├── usd_file/
│   │   └── meshes/
│
├── phyAI_ws/                           # ROS 2 workspace for robot-side execution
│   ├── src/
│   │   ├── cleaner_msgs/
│   │   ├── cleaner_system1/
│   │   ├── cleaner_system2/
│   │   ├── gptapi/
│   │   ├── usb_cam/
│   │   ├── vision_context_builder/
│   │   └── yolov8_ros/
│   ├── cleaner_proj.rviz
│   ├── cleaner_system.yaml
│   ├── nav2_localization_params.yaml
│   ├── slam_toolbox_params.yaml
│   ├── frames_2026-05-22_17.02.54.gv
│   └── frames_2026-05.55_17.02.54.pdf
│
├── docs/
│   └── demo-2026-06-09.webm
│
└── README.md
```
