from typing import Any, Dict


class ExtendsValidationContext:
    def __init__(self):
        self.original_methods: Dict[str, Any] = {}

    def _restore_patched_methods(self):
        for (
            target_class,
            method_name,
            original_method,
        ) in self.original_methods.values():
            setattr(target_class, method_name, original_method)
        self.original_methods.clear()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, traceback):
        self._restore_patched_methods()
        return False
