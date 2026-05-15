class SimLoop:
    def __init__(self, sim_app, world, render: bool = True):
        self.app = sim_app
        self.world = world
        self.render = render

    def _is_running(self) -> bool:
        if hasattr(self.app, "is_running"):
            return self.app.is_running()
        if hasattr(self.app, "raw"):
            return self.app.raw.is_running()
        return False

    def run(self):
        while self._is_running():
            self.world.step(render=self.render)
