from functools import lru_cache
from typing import Any


@lru_cache(maxsize=1)
def get_model():
    """
    Load the BirdNET acoustic model once and keep it in memory.

    The BirdNET package handles model initialization/caching.
    """
    import birdnet

    return birdnet.load("acoustic", "3.0", "onnx")


def identify_bird(
    audio_path: str,
    *,
    min_conf: float = 0.20,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Run local BirdNET inference and normalize its output.

    The adapter intentionally keeps the rest of the application independent
    from the model API, making future model replacement easier.
    """
    model = get_model()
    predictions = model.predict(audio_path)

    if hasattr(predictions, "to_dict"):
        rows = predictions.to_dict("records")
    else:
        rows = list(predictions)

    normalized = []

    for row in rows:
        confidence = float(
            row.get(
                "confidence",
                row.get("score", row.get("prediction", 0.0)),
            )
        )

        if confidence < min_conf:
            continue

        species = str(
            row.get(
                "species_name",
                row.get("species", "Unknown"),
            )
        )

        # BirdNET labels can contain scientific/common-name information.
        # Keep a readable fallback even if the exact label format changes.
        if "_" in species:
            scientific_name, common_name = species.split("_", 1)
        else:
            scientific_name = species
            common_name = species

        normalized.append(
            {
                "common_name": common_name,
                "scientific_name": scientific_name,
                "confidence": round(confidence, 4),
                "start_time": float(row.get("start_time", 0.0)),
                "end_time": float(row.get("end_time", 0.0)),
            }
        )

    normalized.sort(key=lambda x: x["confidence"], reverse=True)

    unique = []
    seen = set()

    for item in normalized:
        key = item["common_name"].lower()

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

        if len(unique) >= top_k:
            break

    return unique
