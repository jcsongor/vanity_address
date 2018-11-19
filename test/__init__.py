from unittest.mock import patch


class Patcher():
    def _patch(self, target):
        patcher = patch(target)
        self.addCleanup(patcher.stop)
        return patcher.start()
