# COLAB PREAMPLE
Prepare google colaboratory by one line of command

## Installation

```python
# from pypi
$ pip install colab-preamble

# alternatively, from github
$ git clone https://github.com/kota7/colab-preamble --depth 1
$ pip install -U ./colab-preample
```


## Usage

```python
import colab_preamble

colab_preample_run(google_cloud_project="<project-id>", mount_drive=True)
# If no need to access google cloud services, no need to provide set google_cloud_project=None
# If no need to mount google drive, set mount_drive=False
```

## Effect

When `google_cloud_project` is given,

- Set the default project ID
    - Run `gcloud config set ...`
    - Set `GOOGLE_CLOUD_PROJECT` env variable
- Open the authentication prompt
- Introduce bigquery magic command `bq`


When `mount_drive` is true,

- Google drive is mounted at '/content/drive'
