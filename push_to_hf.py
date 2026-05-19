import os
from pathlib import Path

from datasets import Audio, load_dataset
from huggingface_hub import HfApi, login
from dotenv import load_dotenv


load_dotenv()

PARQUET_DIR = Path("output_parquet")
HF_REPO_ID = os.getenv("HF_REPO_ID")
HF_TOKEN = os.getenv("HF_TOKEN")


def build_dataset(parquet_dir):
    data_files = {}

    split_candidates = {
        "train": ["train.parquet", "train/*.parquet"],
        "validation": ["validation.parquet", "validation/*.parquet", "valid.parquet", "valid/*.parquet"],
        "test": ["test.parquet", "test/*.parquet"],
    }

    for split_name, candidates in split_candidates.items():
        found = []
        for pattern in candidates:
            matches = sorted(parquet_dir.glob(pattern))
            found.extend(str(path) for path in matches if path.is_file())

        # Deduplicate while preserving order.
        if found:
            data_files[split_name] = list(dict.fromkeys(found))

    if not data_files:
        raise SystemExit(f"No parquet files found in {parquet_dir}")

    return load_dataset("parquet", data_files=data_files)


def main():
    if not HF_REPO_ID:
        raise SystemExit("Missing HF_REPO_ID in .env")

    if HF_TOKEN:
        login(token=HF_TOKEN)
        HfApi().create_repo(repo_id=HF_REPO_ID, repo_type="dataset", exist_ok=True, token=HF_TOKEN)
    else:
        raise SystemExit("Missing HF_TOKEN in .env")

    dataset = build_dataset(PARQUET_DIR.expanduser().resolve())
    dataset = dataset.cast_column("audio", Audio())
    dataset.push_to_hub(HF_REPO_ID)
    print("Pushed dataset to", HF_REPO_ID)


if __name__ == "__main__":
    main()
