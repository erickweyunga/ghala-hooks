import pkgutil
import importlib

def load_plugins(package_path: str) -> None:
    """
    Dynamically import all modules in the given package path.
    Only loads plugins marked as active (PLUGIN_ACTIVE=True or not set).

    Args:
        package_path: Python package path as a string, e.g., "app.plugins"
    """
    try:
        package = importlib.import_module(package_path)
    except ModuleNotFoundError:
        return

    if not hasattr(package, "__path__"):
        return

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        mod = importlib.import_module(f"{package.__name__}.{module_name}")
        active = getattr(mod, "PLUGIN_ACTIVE", True)
        if not active:
            continue
