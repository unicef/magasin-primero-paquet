# magasin_primero - Data ingestion from Primero to a magasin instance

This is a [Dagster](https://dagster.io/) project. Dagster is a pipeline orchestrator, that allows you to define, schedule, and monitor data pipelines. In this project, we use Dagster to ingest data from a Primero instance into a cloud storage (fi. S3 Bucket/MinIO or Azure Blob Storage).

## Pre-requisites

* A primero instance
* A Bucket in S3/MinIO or Azure Blob Storage to store the data.
* Python 3.12

Before modifying the code it is recommended to follow the [get started tutorial of magasin](https://magasin.unicef.io/get-started/). This will help you to understand the basics of magasin.

This pipeline also makes use of the [primero-api library](https://pypi.org/project/primero-api/). This library is a wrapper around the Primero API that is also part of the [magasin-primero-paquet](../README.md).


## Testing the pipeline locally

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

It is recommended to create a [virtual environment](https://docs.python.org/3/library/venv.html) to install the dependencies:

```bash
python -m venv venv # this is only run once
source venv/bin/activate # Run this every time you want to work on the project
```

Then, install the dependencies:

```bash
pip install -e ".[dev]"
```

Edit the `.env` file

```sh
PRIMERO_USER='primero_cp'
PRIMERO_PASSWORD='primero2024'
PRIMERO_API_URL="https://playground.primerodev.org/api/v2/"
ENVIRONMENT='dev'

FSSPEC_S3_ENDPOINT_URL='http://localhost:9000'
FSSPEC_S3_KEY='minio'
FSSPEC_S3_SECRET='minio123'
BUCKET_NAME='primero'

AZURE_STORAGE_CONNECTION_STRING="AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
```

Where 

* The `PRIMERO_USER`, `PRIMERO_PASSWORD`, `PRIMERO_API_URL` are the credentials to connect to the Primero instance. The one in the example is the credentials to connect to the [Primero Playground](https://playground.primerodev.org/).

* The `FSSPEC-S3-*` are the credentials to connect to a S3/MinIO bucket.
* The `BUCKET_NAME` is the name of the bucket/blob container name where the data will be stored.

* The `AZURE_STORAGE_CONNECTION_STRING` is the connection string to connect to an Azure Blob Storage. The one in the example is the connection string to connect to the Azure Storage Emulator using [Microsoft Azure Storage Explorer](https://github.com/microsoft/AzureStorageExplorer).

* The `ENVIRONMENT` is the environment where the pipeline is running. It can be `dev`. Any other value will be considered as 'prod'.

Then, start the Dagster UI web server:

```bash
dagster dev
```
Open **http://localhost:3000** with your browser to see the project.

If you use magasin's minio, you need a bucket called `primero` (through `mag minio add bucket --bucket-name primero`) and you need to forward the port 9000 of the MinIO service into the local machine. You can do this by running the following command in another terminal:

```sh
mag minio api
```

In the source code of `assets.py` here are three [dagster assets](https://docs.dagster.io/concepts/assets/software-defined-assets) defined:

* `cases` that gets all the cases in the /<BUCKET_NAME>/cases/cases.parquet
* `incidents` that gets all the incidents in the /<BUCKET_NAME>/incidents/incidents.parquet
* `reports` that gets all the reports in the /<BUCKET_NAME>/reports/report-{report.id}-{report.slug}/report.parquet'

There is a resource called `primero_api_resource` which basically instantiates a PrimeroAPI object of the [`primero-api` library](../../primero-api/).

### Build the docker image

If you have modified the source code of the `pipelines/magasin_primero` folder and you want to run the pipeline in a magasin instance. You need to build the docker image of your pipeline. 



```shell
cd pipelines/magasin-primero
# ./build.sh <your-docker-username or your.azurecr.io> <tag1> <tag2> 
# Example: 
./build.sh  merlos latest v0.0.1
```
This will create a docker image with the name `merlos/magasin-primero-pipeline:latest` and `merlos/magasin-primero-pipeline:v0.0.1` and push it to the docker hub.



### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Unit testing

Tests are in the `magasin_primero_tests` directory and you can run tests using `pytest`:

```bash
pytest magasin_primero_tests
```

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) or [Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors) for your jobs, the [Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.


# License

MIT License
