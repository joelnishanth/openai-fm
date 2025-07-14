import requests
from typing import List
from PIL import Image
from io import BytesIO
import imagehash
import numpy as np

OLLAMA_URL = "http://localhost:11434"


def _json_rpc(method: str, params: dict):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    resp = requests.post(f"{OLLAMA_URL}/rpc", json=payload)
    resp.raise_for_status()
    return resp.json().get("result")


def compute_image_hash(image_url: str) -> str:
    """Compute perceptual hash for an image URL."""
    r = requests.get(image_url)
    r.raise_for_status()
    img = Image.open(BytesIO(r.content))
    ph = imagehash.phash(img)
    return str(ph)


def compute_text_embedding(text: str) -> List[float]:
    """Get embeddings via Ollama."""
    return _json_rpc("embedding", {"model": "clip", "prompt": text})


def compare_embeddings(vec1: List[float], vec2: List[float]) -> float:
    """Cosine similarity between two vectors."""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def compare_image_hashes(hash1: str, hash2: str) -> float:
    """Compute similarity score between two image hashes."""
    h1 = imagehash.hex_to_hash(hash1)
    h2 = imagehash.hex_to_hash(hash2)
    # convert to similarity (1 - normalized hamming distance)
    distance = (h1 - h2) / len(h1.hash) ** 2
    return 1.0 - distance
