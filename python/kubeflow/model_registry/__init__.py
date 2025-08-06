# Re-export ModelRegistry from the standalone model-registry package
# This allows users to import from kubeflow.model_registry while
# maintaining backward compatibility with the standalone package

try:
    from model_registry import ModelRegistry as ModelRegistryClient
except ImportError as e:
    raise ImportError(
        "model-registry package is required. Install with: pip install model-registry"
    ) from e

__all__ = [
    "ModelRegistryClient",
]
