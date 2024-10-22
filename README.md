# magasin-primero-paquet - Unlock the Full Potential of Your Primero Data

This repository contains the code to ingest, store, and analyze data from Primero using [magasin](https://unicef.github.io/magasin/).

Magasin is a foundational toolset designed to help data analysis teams uncover valuable insights. It enables you to extract, analyze, and visualize data from multiple sources. As the only complete, open-source, cloud-based data and AI toolset, Magasin grows with your organization, empowering you to make better decisions with clear and impactful insights throughout your digital transformation journey. 

**[👉 Learn more about magasin](https://unicef.github.io/magasin/)**

## Pre-requisites

- magasin instance
- Primero instance

## Installation



```shell
# create the minio bucket

mag minio add bucket --bucket-name primero
```


## Repository Structure

This repository is organized following the magasin data lifecycle, that is explained in the [magain getting started tutorial overview](https://unicef.github.io/magasin/get-started/tutorial-overview.html):

- `explorations/`: Contains the code to analyze the data from Primero using Jupyter notebooks, it allows you to get a grasp of what does the dataset contain and play with it using python code..
- `pipelines/`: Contains the code to ingest data from Primero into magasin using Dagster. Using Primero API it extracts data into a cloud storage (fi. S3 Bucket/MinIO or Azure Blob Storage).
- `dashboards/`: Contains the SuperSet dashboards to visualize the data from Primero.

Additionally 
- `primero_api/`: Contains the code to interact with the Primero API using Python.

# LICENSE
This repository is licensed under the MIT License. 
