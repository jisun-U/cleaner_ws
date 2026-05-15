from omni.isaac.core.utils.stage import open_stage
from omni.isaac.core import World
from omni.isaac.core.articulations import ArticulationView
from omni.isaac.core.utils.prims import define_prim
from pxr import UsdGeom, Sdf

# app/world.py 등 공용 유틸에 넣어두면 좋음
import omni.usd, omni.kit.app, omni.kit.commands as kitcmd
from pxr import Gf, Sdf

class SimWorld:
    # cleaner_prim: cleaner articulation을 찾기 위한 USD 경로 문자열
    def __init__(self, usd_path: str, cleaner_prim: str, imu_dummy_prim: str,
                 fixed_time_step: bool, play_every_frame: bool, target_hz: int,
                 lidar_cfg: dict | None = None, articulation_root: str | None = None):
        
        import omni.usd
        import omni.timeline
        import carb.settings

        open_stage(usd_path) #stage 오픈
        self.stage = omni.usd.get_context().get_stage() 
        #로봇을 물리 시뮬레이션의 아티큘레이션과 연결 
        #-> 물리 엔진이 로봇을 관절이 있는(제어가 가능한) 객체로 인식하도록 함

        # 아티큘레이션 루트 프림을 찾는 헬퍼 함수
        def _has_articulation_root_api(prim) -> bool:
            from pxr import UsdPhysics
            try:
                if prim.HasAPI(UsdPhysics.ArticulationRootAPI):
                    return True
            except Exception:
                pass
            try:
                applied = prim.GetAppliedSchemas()
            except Exception:
                applied = []
            return "PhysicsArticulationRootAPI" in applied or "ArticulationRootAPI" in applied

        def _find_articulation_root(stage, base_path: str, explicit_path: str | None) -> str | None:
            from pxr import Usd

            if explicit_path:
                explicit = stage.GetPrimAtPath(explicit_path)
                if explicit.IsValid():
                    if _has_articulation_root_api(explicit):
                        return explicit.GetPath().pathString
                    print(f"[SimWorld] WARNING: explicit articulation root exists but has no ArticulationRootAPI: {explicit_path}")

            base = stage.GetPrimAtPath(base_path)
            if not base.IsValid():
                return None

            if _has_articulation_root_api(base):
                return base.GetPath().pathString

            it = Usd.PrimRange(base)
            for prim in it:
                if prim.IsValid() and _has_articulation_root_api(prim):
                    return prim.GetPath().pathString
            return None

        settings = carb.settings.acquire_settings_interface()
        timeline = omni.timeline.get_timeline_interface() #시간 및 타임라인 고정
        if fixed_time_step:
            settings.set("/app/player/useFixedTimeStepping", True)
        timeline.set_play_every_frame(play_every_frame)
        settings.set("/app/player/targetRunLoopFrequency", int(target_hz))
        timeline.play()
        
        # define_prim("/World/odom", "Xform") 없다면 삽입
        cleaner_root = _find_articulation_root(self.stage, cleaner_prim, articulation_root)

        self.world = World()
        self.world.reset()

        if not cleaner_root:
            #cleaner_prim아래에 articulation root를 찾음
            print(f"[SimWorld] Available prims under '{cleaner_prim}':")
            base = self.stage.GetPrimAtPath(cleaner_prim)
            if base.IsValid():
                from pxr import Usd
                for i, prim in enumerate(Usd.PrimRange(base)):
                    if i >= 80:
                        print("[SimWorld] ...")
                        break
                    print(f"  {prim.GetPath().pathString} schemas={prim.GetAppliedSchemas()}")
            raise RuntimeError(f"[SimWorld] Could not find ArticulationRoot under '{cleaner_prim}'")
        # ArticulationView로 물리 엔진과 연결
        self.cleaner = ArticulationView(prim_paths_expr=cleaner_root, name="cleaner_view")
        self.world.scene.add(self.cleaner)
        self.world.play()

    def step(self, render=True):
        self.world.step(render=render)
