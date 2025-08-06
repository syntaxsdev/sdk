import pytest
import sys


@pytest.mark.model_registry
def test_import_model_registry_available():
    """Test that ModelRegistry can be imported when model-registry package is available."""
    try:
        from kubeflow.model_registry import ModelRegistry, ModelRegistryClient
        from model_registry import ModelRegistry as OriginalModelRegistry

        # Verify they are the same class
        assert ModelRegistry is OriginalModelRegistry
        assert ModelRegistryClient is OriginalModelRegistry

    except ImportError:
        pytest.skip("model-registry package is not installed")


@pytest.mark.model_registry
def test_import_model_registry_client_available():
    """Test that ModelRegistryClient is an alias for ModelRegistry."""
    try:
        from kubeflow.model_registry import ModelRegistryClient, ModelRegistry

        # Verify ModelRegistryClient is an alias for ModelRegistry
        assert ModelRegistryClient is ModelRegistry

    except ImportError:
        pytest.skip("model-registry package is not installed")


@pytest.mark.model_registry
def test_import_error_when_model_registry_not_installed(monkeypatch):
    """Test that a helpful error is raised when model-registry is not available."""
    # Remove the module from sys.modules if it exists
    modules_to_remove = ["kubeflow.model_registry", "model_registry", "model_registry._client"]
    original_modules = {}

    for module_name in modules_to_remove:
        if module_name in sys.modules:
            original_modules[module_name] = sys.modules[module_name]
            del sys.modules[module_name]

    # Store the original import function to avoid recursion
    original_import = __import__

    def mock_import(name, *args, **kwargs):
        if name == "model_registry":
            raise ImportError("No module named 'model_registry'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", mock_import)

    try:
        with pytest.raises(ImportError) as exc_info:
            import kubeflow.model_registry  # noqa: F401

        # Verify the error message is helpful
        assert "model-registry package is required" in str(exc_info.value)
        assert "pip install model-registry" in str(exc_info.value)

    finally:
        # Restore the original modules
        for module_name, module in original_modules.items():
            sys.modules[module_name] = module


@pytest.mark.model_registry
def test_all_exports_available():
    """Test that all expected exports are available in the module."""
    try:
        import kubeflow.model_registry as mr_module

        # Check that __all__ contains expected items
        expected_exports = ["ModelRegistry", "ModelRegistryClient"]
        assert hasattr(mr_module, "__all__")
        assert set(mr_module.__all__) == set(expected_exports)

        # Check that all items in __all__ are actually available
        for export in expected_exports:
            assert hasattr(mr_module, export)

    except ImportError:
        pytest.skip("model-registry package is not installed")


@pytest.mark.model_registry
def test_import_via_star_import():
    """Test that star imports work correctly."""
    try:
        # This is a bit tricky to test directly, so we'll check the namespace
        import kubeflow.model_registry as mr_module

        # Simulate what 'from kubeflow.model_registry import *' would do
        star_imports = {name: getattr(mr_module, name) for name in mr_module.__all__}

        assert "ModelRegistryClient" in star_imports
        assert star_imports["ModelRegistry"] is star_imports["ModelRegistryClient"]

    except ImportError:
        pytest.skip("model-registry package is not installed")
