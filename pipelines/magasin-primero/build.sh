#!/bin/bash
#
# Magasin Primero Pipeline Build Script
#
# This script builds the magasin-primero dagster pipeline image for both amd64 and arm64 architectures.
#
# It uses the buildx feature of docker to build for multiple architectures.
#
# Usage,
#  * The script assumes that the docker daemon is running and that the user has the necessary permissions to run docker commands.
#  * The script also assumes that the user has logged in to the registry where the image will be pushed.
#  * The script takes the registry as an argument. The registry is the location where the image will be pushed.
#  * The registry can be a docker hub username or a registry URL.
#
# Example: ./build.sh my-registry.azurecr.io
#          ./build.sh my-docker-hub-username
#
# Adding tags to the image. By default latest is added
# Example with tags : ./build.sh merlos latest v1.0.0
# 


# Get registry from the command line
REGISTRY=$1

# Check if the registry is empty
if [ -z "$REGISTRY" ]
then
  echo "Registry is empty. Please provide a registry"
  exit 1
fi 

# Optionally add tags to the image
TAGS=${@:2}
if [ -z "$TAGS" ]
then
  TAGS="latest"
fi

# first we create a builder. This just allows us to build for architectures different that our owns.
# This only needs to be run once per computer.
docker buildx create --driver=docker-container --name=magasin-builder 

# Prepare the tag options for the docker buildx command
TAG_OPTIONS=""
for TAG in $TAGS; do
  TAG_OPTIONS="$TAG_OPTIONS -t $REGISTRY/magasin-primero-pipeline:$TAG"
done

# In the command below replace <registry> by your registry.
# If you are using docker hub, it is your user name (you need to login first.
# In other registries such as Azure Container Registry (my-registry.azurecr.io)or Amazon ECR, please check the documentation of the provider.
set -x
docker buildx build --builder=magasin-builder --platform linux/amd64,linux/arm64 $TAG_OPTIONS --push .