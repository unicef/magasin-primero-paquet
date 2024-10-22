
# How to run primero locally

This is a quick guide on how to setup primero for testing locally using docker & docker compose.

First build the images

```shell
git clone https://github.com/primeroIMS/primero
```

One may need to remove the security packages if not updated in `nginx/Dockerfile` the following line if the values are not updated
```
ENV SECURITY_UPDATED_PACKAGES=""
```


```shell
cd primero/docker
./build.sh all
```

Copy local.env.sample.local to local.env

Add
```shell 
PRIMERO_MESSAGE_SECRET=PRIMERO_MESSAGE_SECRET
```

Replace the this in the application dockerfile
```Dockerfile

ENV BUILD_PACKAGES="bash curl wget curl-dev build-base git gcompat" # Add gcompat

# Run bundle install  --- Replace the run command with the following
RUN set -euox pipefail \
        ; if [ $RAILS_ENV == "production" ]; \
        then \
        export BUNDLER_WITHOUT="development test" \
        ; else \
        export BUNDLER_WITHOUT="" \
        ; fi \
        && apk update && apk add gcompat \
        && bundle install  \
        #echo "Bundler install complete"
        && gem install nokogiri --platform=ruby \ 
        && bundle info nokogiri  \
        #&& ls /usr/local/bundle/gems/nokogiri-1.16.5-aarch64-linux/lib/nokogiri/3.3/ \
        && bundle lock --add-platform=arm64-linux \
        && bundle platform \
        && ruby -e 'puts Gem::Platform.local.to_s'
```


Build 
```shell
./compose.configure.sh
./compose.prod.sh up -d
```

Access the application container and run  to populate the database

To populate the database:

Open a shell in the primero/application container. Go to the folder `/srv/primero/application/`
and run:

```sh
rails db:seed
rails r ./db/dev_fixtures/cases_and_families.rb true 11000
```

Now open: 
http://localhost


User and password: `primero/primer0!`



----
Information related with nokogiri issue
https://github.com/github/pages-gem/issues/839

https://nokogiri.org/tutorials/installing_nokogiri.html#linux-musl-error-loading-shared-library










----------------

# How the primero helm chart was created


# Build the images

The first thing is to build the images.
Primero has several custom docker images tha


Cloned the repo

```shell
git clone https://github.com/primeroIMS/primero
```
The repo is in the ./primero directory.

cd primero/docker

# Build the images

```shell
./build.sh all
```


Create the new helm chart.

```shell
mkdir primero-helm
cd primero-helm
helm create primero
```
This creates a scaffold for the helm chart in the directory `./primero-helm/primero`.


