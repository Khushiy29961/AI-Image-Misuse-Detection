import hashlib

def generate_dna_fingerprint(image_bytes):
    """Generates a unique SHA-256 hash for the image evidence."""
    sha256_hash = hashlib.sha256(image_bytes).hexdigest()
    return sha256_hash