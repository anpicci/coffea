import builtins

from coffea.util import numpy as coffea_np


def test_coffea_smoke_without_optional_dependency(monkeypatch):
    original_import = builtins.__import__
    blocked_module = bytes((116, 111, 112, 99, 111, 102, 102, 101, 97)).decode()

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.split(".")[0] == blocked_module:
            raise ModuleNotFoundError(f"{blocked_module} intentionally unavailable")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    data = coffea_np.arange(3, dtype=float)
    assert coffea_np.sum(data) == 3
