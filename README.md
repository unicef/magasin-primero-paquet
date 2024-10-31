# magasin-primero-paquet - Unlock the Full Potential of Your Primero Data

This repository contains the code to ingest, store, analyze and visualize data from [Primero](https://www.primero.org), the open-source child protection case management system, using [magasin](https://magasin.unicef.io).

As a result of setting up this _paquet_ you will have a dashboard with insights about the cases and incidents of primero that gets fresh data from your Primero instance every day. 

    TODO - Add a screenshot of the dashboard

Alternatively, if you want do data explorations with the data extracted from Primero you can use the [Jupyter notebook](./explorations/primero.ipynb) in the `explorations/` folder. 

## What is Magasin?

Magasin is a foundational toolset designed to help data analysis teams uncover valuable insights. It enables organizations to extract, analyze, and visualize data from multiple sources. As the only complete, open-source, cloud-based data and AI toolset, Magasin grows with your organization, empowering you to make better decisions with clear and impactful insights throughout your digital transformation journey. 

👉 **[Learn more about magasin](https://magasin.unicef.io/)**

## Pre-requisites

In order to get the full potential, ie. to have a full dashboard, you need to have:

- [A magasin instance](https://magasin.unicef.io/get-started/). For testing purposes you can install magasin in a regular computer.
- Credentials to log into a Primero 2.x instance.

Experience with command line and python programming language may be useful. 

It is also recommended to have followed the [magasin getting started tutorial](https://unicef.github.io/magasin/get-started/tutorial-overview.html) before trying to install this _paquet_. It will give you a better understanding of the magasin data analysis lifecycle.

## Contents & Repository Structure

This repository is organized following the magasin data analysis lifecycle, that is explained in the [magain getting started tutorial overview](https://unicef.github.io/magasin/get-started/tutorial-overview.html), in which you start [exploring](./explorations/) the data to get valuable insights, then you ingest the data into magasin using [automated pipelines](./pipelines/), and finally you visualize the data using [dashboards](./dashboards/).

So, the repository is organized as follows:

- `explorations/`: Contains some sample code that allows you to analyze the data from Primero using a simple Jupyter notebooks, it allows you to get a grasp of what does the dataset contain and play with it using python code.
- `pipelines/`: Contains the code to ingest data from Primero into magasin using Dagster. Using Primero API it extracts data into a cloud storage (fi. S3 Bucket/MinIO or Azure Blob Storage).
- `dashboards/`: Contains the SuperSet dashboards to visualize the data from Primero.

Additionally 
- `primero_api/`: Contains the a python library to interact with the Primero API.


## Installation

In the computer from which you want to perform the installation of the `magasin-primero-paquet` you need to have also installed `kubectl` and `mag-cli`. You can use the following commands to install them:

```shell
# Debian/Ubuntu / Windows WSL
curl -sSL http://magasin.unicef.io/install-magasin.sh | bash -s -- -i 
# MacOS
curl -sSL http://magasin.unicef.io/install-magasin.sh | zsh -s -- -i 
```

## Step 1 - Setup the storage

First you need to setup the cloud storage where the data extracted from Primero will be stored. You can use either S3 Bucket, MinIO or Azure Blob Storage. 

By default magasin includes MinIO. To create a MinIO bucket you can use the following command:

```shell
# create the minio bucket
mag minio add bucket --bucket-name primero
```

## Step 2 - Setup the data ingestion pipeline.

    TODO - Add the instructions to setup the pipeline


Check the content of the bucket using the following command:

```shell
mc ls myminio/primero 
```
You can copy them locally and check the content:

```shell
mc cp myminio/primero .
```

We use [parquet files](https://parquet.apache.org/) to store the data extracted from Primero. To see the content of this files you can use [parquet viewer in Windows](https://github.com/mukunku/ParquetViewer) and [Tad in OSX, Linux and Windows](https://www.tadviewer.com/)


## Step 3 - Setup the dashboard

Once you have the data in the cloud storage you can setup the dashboard to visualize the data. 

    TODO - Add the instructions to setup the dashboard

# LICENSE
This repository is licensed under the MIT License. 

Copyright (c) 2024 UNICEF

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.