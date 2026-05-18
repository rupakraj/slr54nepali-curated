# Curated Open SLR Nepali Dataset (SLR54 - Nepali)

Curated release of the [OpenSLR SLR54 Nepali](https://openslr.trmal.net/resources/54/about.html) speech dataset prepared for academic experiments.

## Why?
The original source, [Large Nepali ASR training data set(SLR54)](https://www.openslr.org/54/)
, does not provide a recommended train/validation/test split. This makes it difficult to fairly evaluate and compare work that uses this dataset.

The purpose of this repository is to share a standardized dataset split and provide a Hugging Face–compatible version of the dataset.


## Dataset summary
- **Language:** Nepali
- **Source:** Open SLR (SLR54) — curated subset prepared locally
- **Files included:** `train.tsv`, `valid.tsv`, `test.tsv` (tab-separated: file_id, speaker_id, transcript)


Local layout expected by the scripts
- TSV files in the root folder or in the directory passed with `--tsv-dir`
- Audio files at `<root>/<split>/<speaker_id>/<file_id>.wav`

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

`.env` file

```bash
# .env
WAV_ROOT_PATH=<path to the wav file>
HF_TOKEN=="<your_token>"
```

2. Convert TSV + audio into parquet shards:

```bash
python create_parquet.py
```

3. Push the parquet dataset to the Hub (replace `USERNAME/REPO_NAME`):

```bash
python push_to_hf.py --repo-id USERNAME/slr54-nepali-curated --token $HF_TOKEN --parquet-dir parquet
```

Script details
- `create_parquet.py` embeds audio bytes into parquet files so the uploaded dataset is independent of source file paths.
- `push_to_hf.py` loads the parquet files and calls `push_to_hub()`.


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
