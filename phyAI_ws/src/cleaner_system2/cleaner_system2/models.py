# cleaner_system2/models.py
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field # pydantic : 데이터가 우리가 정한 규칙에 맞는지 검사함


class Step(BaseModel):
    task: Literal[ # Literal : 허용된 task 종류 이외가 들어오면 error
        "move_to",
        "scan",
        "track",
        "return_to_home",
        "cleaner_mode",
    ]
    params: Dict[str, Any] = Field(default_factory=dict)
    guard: Optional[str] = None
    retry: int = Field(0, ge=0)  # ge : greater than or equal to 0, 음수면 안됨


class ReplanRules(BaseModel): # 미션 수행 중 돌발상황 발생시 대처방식
    lost_target_sec: float = 5.0
    battery_rtb: float = Field(0.18, ge=0.0, le=1.0)
    hard_stuck_timeout_sec: float = 20.0
    # 추가 필드들은 스키마상으로 허용(additionalProperties=True)이지만
    # 지금은 명시적으로 안 쓰고, 들어와도 그냥 무시되는 상태(pydantic 기본 extra="ignore")


class HighLevelPlan(BaseModel): # system2가 만들어내는 최종 고수준 plan
    #  스키마의 const: "1.0.0" 에 맞춤
    version: Literal["1.0.0"] = "1.0.0"

    mission_id: str
    intent: str
    constraints: List[str] = Field(default_factory=list)
    steps: List[Step]
    replan_rules: ReplanRules = ReplanRules()


class VisionSnapshot(BaseModel):
    summary: Optional[str] = None


class System1State(BaseModel):
    mission_id: Optional[str] = None
    system1_state: Optional[str] = None
    current_task: Optional[str] = None
    step_index: Optional[int] = None
    pose: Optional[Dict[str, float]] = None
    vision_snapshot: Optional[VisionSnapshot] = None
    notes: Optional[str] = None
