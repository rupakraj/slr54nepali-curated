# Curated Open SLR Nepali Dataset (SLR54 - Nepali)

Curated release of the [OpenSLR SLR54 Nepali](https://openslr.trmal.net/resources/54/about.html) speech dataset prepared for academic experiments.

## Why?
The original source, [Large Nepali ASR training data set(SLR54)](https://www.openslr.org/54/)
, does not provide a recommended train/validation/test split. This makes it difficult to fairly evaluate and compare work that uses this dataset.

The purpose of this repository is to share a proper dataset split and convert the dataset to a Hugging Face–compatible version of the dataset.

## Where to find the data?
This repo only hosts the `{split}.tsv` files. The audio resouce are hosted in hugging face.

Hugging face: [rughimire/slr54nepali-curated](https://huggingface.co/datasets/rughimire/slr54nepali-curated)


## Dataset summary
- **Language:** Nepali
- **Source:** Open SLR (SLR54) — curated subset prepared locally
- **Files included:** `train.tsv`, `valid.tsv`, `test.tsv` (tab-separated: file_id, speaker_id, transcript)


## How to use?

Todo

## How to create Hugging Face Dataset?

1. Install dependencies

```bash
python -m venv venv
source ./venv/bin/active
pip install -r requirements.txt
```

The logic and other details should be in `.env` file.

```bash
# .env
WAV_ROOT_PATH="<path to wav files>"
PARQUET_SHARD_SIZE_MB=1024
HF_REPO_ID=rughimire/slr54nepali-curated
HF_TOKEN=<your_token>
```
__note__: The script will source the `.env` file.

2. Convert TSV + audio into parquet shards

```bash
python create_parquet.py
```

3. Push the parquet dataset to the Hub

```bash
python push_to_hf.py
```

Script details
- `create_parquet.py` stores each audio example as a `{bytes, path}` struct so the dataset stays independent of source paths.
- `push_to_hf.py` casts the `audio` column to `datasets.Audio` before pushing, which is what enables playback in the Hugging Face dataset viewer.

If the dataset viewer still shows raw bytes, re-upload after regenerating the parquet shards with the updated script and make sure the `audio` column is present.


## Original Dataset
- Get the original dataset into the : https://www.openslr.org/54/
- License: Attribution-ShareAlike 4.0 International - [read](https://openslr.trmal.net/resources/54/LICENSE)


## Citation
Please cite the original paper whenever this dataset are being used:

```
@inproceedings{kjartansson-etal-sltu2018,
    title = {{Crowd-Sourced Speech Corpora for Javanese, Sundanese,  Sinhala, Nepali, and Bangladeshi Bengali}},
    author = {Oddur Kjartansson and Supheakmungkol Sarin and Knot Pipatsrisawat and Martin Jansche and Linne Ha},
    booktitle = {Proc. The 6th Intl. Workshop on Spoken Language Technologies for Under-Resourced Languages (SLTU)},
    year  = {2018},
    address = {Gurugram, India},
    month = aug,
    pages = {52--55},
    URL   = {http://dx.doi.org/10.21437/SLTU.2018-11}
  }
```
