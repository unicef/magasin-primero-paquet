# magasin_primero - Data ingestion from Primero to a magasin instance


This is a [Dagster](https://dagster.io/) project. Dagster is a pipeline orchestrator, that allows you to define, schedule, and monitor data pipelines. In this project, we use Dagster to ingest data from a Primero instance into a cloud storage (fi. S3 Bucket/MinIO or Azure Blob Storage).

## Pre-requisites

* A primero instance
* A Bucket in S3/MinIO or Azure Blob Storage to store the data.



## Testing the pipeline locally

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.


It is recommended to create a [virtual environment](https://docs.python.org/3/library/venv.html) to install the dependencies:

```bash
python -m venv venv # this is only run once
source venv/bin/activate # Run this every time you want to work on the project
```


Then, install the dependencies:
```

```bash
pip install -e ".[dev]"
```

Update the configuration




Then, start the Dagster UI web server:

```bash
dagster dev
```
Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `magasin_primero/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.

## Development

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
