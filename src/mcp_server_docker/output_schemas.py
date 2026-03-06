from typing import Any

from docker.models.containers import Container
from docker.models.images import Image
from docker.models.networks import Network
from docker.models.volumes import Volume


def docker_to_dict(
    obj: Image | Container | Volume | Network, overrides: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Convert a Docker SDK model object to a JSON-serializable dict for MCP tool responses.
    Supports Image, Container, Network, and Volume. Optional overrides merge into the result.
    """
    result: dict[str, Any] | None = None

    if isinstance(obj, Image):
        img_config: dict[str, Any] = obj.attrs.get("Config") or {}

        result = {
            "id": obj.id,
            "tags": obj.tags or [],
            "short_id": obj.short_id,
            "labels": img_config.get("Labels") or {},
            "repo_tags": obj.attrs.get("RepoTags") or [],
            "repo_digests": obj.attrs.get("RepoDigests") or [],
            "created": obj.attrs.get("Created"),
            "size": obj.attrs.get("Size"),
        }

    elif isinstance(obj, Container):
        config: dict[str, Any] = obj.attrs.get("Config") or {}
        network_settings: dict[str, Any] = obj.attrs.get("NetworkSettings") or {}
        ports = obj.ports or network_settings.get("Ports") or {}

        result = {
            "id": obj.id,
            "name": obj.name,
            "short_id": obj.short_id,
            "image": docker_to_dict(obj.image) if obj.image else None,
            "image_id": config.get("Image"),
            "status": obj.status,
            "labels": config.get("Labels") or {},
            "ports": ports,
            "created": obj.attrs.get("Created"),
            "state": obj.attrs.get("State"),
            "restart_count": obj.attrs.get("RestartCount"),
            "networks": list((network_settings.get("Networks") or {}).keys()),
            "mounts": obj.attrs.get("Mounts") or [],
            "config": {
                "hostname": config.get("Hostname"),
                "user": config.get("User"),
                "image": config.get("Image"),
            },
        }

    elif isinstance(obj, Network):
        result = {
            "id": obj.id,
            "name": obj.name,
            "short_id": obj.short_id,
            "driver": obj.attrs.get("Driver"),
            "scope": obj.attrs.get("Scope"),
            "created": obj.attrs.get("CreatedAt"),
            "labels": obj.attrs.get("Labels") or {},
        }

    elif isinstance(obj, Volume):
        result = {
            "id": obj.id,
            "name": obj.name,
            "short_id": obj.short_id,
            "labels": obj.attrs.get("Labels") or {},
            "mountpoint": obj.attrs.get("Mountpoint"),
            "created": obj.attrs.get("CreatedAt"),
            "driver": obj.attrs.get("Driver"),
            "scope": obj.attrs.get("Scope"),
        }

    if result is None:
        raise ValueError(f"Unsupported object type: {type(obj)}")

    return result if overrides is None else {**result, **overrides}
