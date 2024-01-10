from waffle_utils.hook import BaseHook


class BaseAdapter(BaseHook):
    def on_loop_start(self, total_steps: int):
        pass

    def on_loop_end(self):
        pass

    def on_step_start(self):
        pass

    def on_step_end(self, current_step: int):
        pass
