import os

from dotenv import load_dotenv
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm


SPLIT_NAMES = {
    "valid": "valid",
    "test": "test",
    "train": "train",
}

load_dotenv()


def read_split_tsv(tsv_path):
    frame = pd.read_csv(
        tsv_path,
        sep="\t",
        header=None,
        names=["file_id", "speaker_id", "transcript"],
        dtype=str,
        keep_default_na=False,
    )
    return frame.fillna("")


def build_parquet_rows(tsv_path, audio_root, split_name):
    frame = read_split_tsv(tsv_path)
    rows = []
    records = frame.to_dict(orient="records")

    for record in tqdm(records, desc=f"{split_name} rows", unit="row"):
        file_id = str(record["file_id"])
        speaker_id = str(record["speaker_id"])
        transcript = str(record["transcript"])

        audio_path = audio_root / split_name / speaker_id / f"{file_id}.wav"
        if not audio_path.exists():
            print(f"Warning: Audio file not found for record {file_id} at {audio_path}, skipping this record.")
            continue

        rows.append(
            {
                "file_id": file_id,
                "speaker_id": speaker_id,
                "transcript": transcript,
                "audio_format": audio_path.suffix.lstrip(".").lower(),
                "audio": audio_path.read_bytes(),
            }
        )
    return rows


def estimate_row_size(row):
    # Approximate per-row bytes to keep shard sizes manageable.
    return (
        len(row.get("audio", b""))
        + len(str(row.get("file_id", "")).encode("utf-8"))
        + len(str(row.get("speaker_id", "")).encode("utf-8"))
        + len(str(row.get("transcript", "")).encode("utf-8"))
        + 1024
    )


def write_rows_to_shard(rows, shard_path):
    table = pa.Table.from_pylist(rows)
    shard_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, shard_path)


def write_parquet_shards(rows, output_dir, split_name, max_shard_size_mb=512):
    max_shard_size_bytes = int(max_shard_size_mb * 1024 * 1024)
    split_dir = output_dir / split_name
    split_dir.mkdir(parents=True, exist_ok=True)

    shard_paths = []
    current_rows = []
    current_size = 0
    shard_index = 0

    for row in rows:
        row_size = estimate_row_size(row)

        if current_rows and (current_size + row_size > max_shard_size_bytes):
            shard_path = split_dir / f"{split_name}-{shard_index:05d}.parquet"
            write_rows_to_shard(current_rows, shard_path)
            shard_paths.append(shard_path)
            current_rows = []
            current_size = 0
            shard_index += 1

        current_rows.append(row)
        current_size += row_size

    if current_rows:
        shard_path = split_dir / f"{split_name}-{shard_index:05d}.parquet"
        write_rows_to_shard(current_rows, shard_path)
        shard_paths.append(shard_path)

    return shard_paths



def main():
    audio_root = Path(os.getenv("WAV_ROOT_PATH", ""))
    max_shard_size_mb = int(os.getenv("PARQUET_SHARD_SIZE_MB", "512"))

    # tsv will be in the current directory by default
    tsv_dir = Path.cwd()
    output_dir = Path.cwd() / "output_parquet"

    created_files = []
    for split_name, parquet_split_name in SPLIT_NAMES.items():
        tsv_path = tsv_dir / f"{split_name}.tsv"
        if not tsv_path.exists():
            print(f"Warning: TSV file for split '{split_name}' not found at {tsv_path}, skipping this split.")
            continue

        rows = build_parquet_rows(tsv_path, audio_root, split_name)
        shard_paths = write_parquet_shards(rows, output_dir, parquet_split_name, max_shard_size_mb=max_shard_size_mb)
        created_files.extend(shard_paths)
        print(f"Wrote {split_name} : {len(rows)} rows into {len(shard_paths)} shard(s) under {output_dir / parquet_split_name}")

    if not created_files:
        print(f"Warning: No TSV files found in {tsv_dir}")


if __name__ == "__main__":
    main()
