from typing import Dict, Any, List


def _extract_hash(value: Any) -> Any:
    """
    Helper to extract comparable 'hash' value.
    If baseline values are simple strings -> returns value.
    If baseline values are dicts like {'hash': '...', 'meta': ...} -> returns value['hash'].
    Keeps comparison robust across small schema changes.
    """
    if isinstance(value, dict) and "hash" in value:
        return value["hash"]
    return value


def compare_baselines(old_baseline: Dict[str, Any], new_baseline: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Compare two baseline dictionaries and return created/modified/deleted file lists.

    Args:
        old_baseline: mapping of file_path -> hash_or_meta (previous snapshot)
        new_baseline: mapping of file_path -> hash_or_meta (fresh snapshot)

    Returns:
        dict with keys 'MODIFIED', 'CREATED', 'DELETED', each mapping to a sorted list of file paths.
    """
    if not isinstance(old_baseline, dict) or not isinstance(new_baseline, dict):
        raise TypeError("Both old_baseline and new_baseline must be dictionaries")

    old_keys = set(old_baseline.keys())
    new_keys = set(new_baseline.keys())

    created = sorted(new_keys - old_keys)
    deleted = sorted(old_keys - new_keys)

    # For common keys, compare extracted hash values (robust to value being dict with 'hash')
    common_keys = old_keys & new_keys
    modified = sorted(
        k for k in common_keys
        if _extract_hash(old_baseline[k]) != _extract_hash(new_baseline[k])
    )

    return {
        "MODIFIED": modified,
        "CREATED": created,
        "DELETED": deleted,
    }


# Quick local test when running this file directly
if __name__ == "__main__":
    old = {
        "/file1.txt": "abc123",
        "/file2.txt": {"hash": "h2", "size": 1234},
        "/file3.txt": "zzz"
    }
    new = {
        "/file1.txt": "abc123",
        "/file2.txt": {"hash": "h2-modified", "size": 1240},
        "/file4.txt": "newone"
    }
    print(compare_baselines(old, new))
    # Expected:
    # {'MODIFIED': ['/file2.txt'], 'CREATED': ['/file4.txt'], 'DELETED': ['/file3.txt']}
