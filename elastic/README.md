# Elastic stack (ELK) on Docker

Based on the official Docker images from Elastic:

* [Elasticsearch](https://github.com/elastic/elasticsearch/tree/master/distribution/docker)
* [Logstash](https://github.com/elastic/logstash/tree/master/docker)
* [Kibana](https://github.com/elastic/kibana/tree/master/src/dev/build/tasks/os_packages/docker_generator)


## Contents

1. [Requirements](#requirements)
   * [Host setup](#host-setup)
   * [Docker Desktop](#docker-desktop)
     * [Windows](#windows)
     * [macOS](#macos)
1. [Usage](#usage)
   * [Bringing up the stack](#bringing-up-the-stack)
   * [Initial setup](#initial-setup)
     * [Setting up user authentication](#setting-up-user-authentication)
   * [Cleanup](#cleanup)
1. [Configuration](#configuration)
   * [How to configure Elasticsearch](#how-to-configure-elasticsearch)
   * [How to configure Kibana](#how-to-configure-kibana)
   * [How to configure Logstash](#how-to-configure-logstash)
   * [How to disable paid features](#how-to-disable-paid-features)
   * [How to scale out the Elasticsearch cluster](#how-to-scale-out-the-elasticsearch-cluster)
   * [How to reset a password programmatically](#how-to-reset-a-password-programmatically)
1. [Extensibility](#extensibility)
   * [How to add plugins](#how-to-add-plugins)
   * [How to enable the provided extensions](#how-to-enable-the-provided-extensions)
1. [Going further](#going-further)
   * [Plugins and integrations](#plugins-and-integrations)

## Requirements

### Host setup

* [Docker Engine](https://docs.docker.com/install/) version **18.06.0** or newer
* [Docker Compose](https://docs.docker.com/compose/install/) version **1.26.0** or newer
* 1.5 GB of RAM

*:information_source: Especially on Linux, make sure your user has the [required permissions][linux-postinstall] to
interact with the Docker daemon.*

By default, the stack exposes the following ports:

* 5044: Logstash Beats input
* 5000: Logstash TCP input
* 9600: Logstash monitoring API
* 9200: Elasticsearch HTTP
* 9300: Elasticsearch TCP transport
* 5601: Kibana

**:warning: Elasticsearch's [bootstrap checks][booststap-checks] were purposely disabled to facilitate the setup of the
Elastic stack in development environments. For production setups, we recommend users to set up their host according to
the instructions from the Elasticsearch documentation: [Important System Configuration][es-sys-config].**

### Docker Desktop

#### Windows

If you are using the legacy Hyper-V mode of _Docker Desktop for Windows_, ensure [File Sharing][win-filesharing] is
enabled for the `C:` drive.

#### macOS

The default configuration of _Docker Desktop for Mac_ allows mounting files from `/Users/`, `/Volume/`, `/private/`,
`/tmp` and `/var/folders` exclusively. Make sure the repository is cloned in one of those locations or follow the
instructions from the [documentation][mac-filesharing] to add more locations.

## Usage

**:warning: You must rebuild the stack images with `docker-compose build` whenever you switch branch or update the
[version](#version-selection) of an already existing stack.**

### Bringing up the stack

Clone this repository onto the Docker host that will run the stack, then start the stack's services locally using Docker
Compose:

```console
$ docker-compose up
```

*:information_source: You can also run all services in the background (detached mode) by appending the `-d` flag to the
above command.*

Give Kibana about a minute to initialize, then access the Kibana web UI by opening <http://localhost:5601> in a web
browser and use the following (default) credentials to log in:

* user: *elastic*
* password: *changeme*

*:information_source: Upon the initial startup, the `elastic`, `logstash_internal` and `kibana_system` Elasticsearch
users are intialized with the values of the passwords defined in the [`.env`](.env) file (_"changeme"_ by default). The
first one is the [built-in superuser][builtin-users], the other two are used by Kibana and Logstash respectively to
communicate with Elasticsearch. This task is only performed during the _initial_ startup of the stack. To change users'
passwords _after_ they have been initialized, please refer to the instructions in the next section.*

### Initial setup

#### Setting up user authentication

*:information_source: Refer to [Security settings in Elasticsearch][es-security] to disable authentication.*

**:warning: Starting with Elastic v8.0.0, it is no longer possible to run Kibana using the bootstraped privileged
`elastic` user.**

The _"changeme"_ password set by default for all aforementioned users is **unsecure**. For increased security, we will
reset the passwords of all aforementioned Elasticsearch users to random secrets.

1. Reset passwords for default users

    The commands below resets the passwords of the `elastic`, `logstash_internal` and `kibana_system` users. Take note
    of them.

    ```console
    $ docker-compose exec elasticsearch bin/elasticsearch-reset-password --batch --user elastic
    ```

    ```console
    $ docker-compose exec elasticsearch bin/elasticsearch-reset-password --batch --user logstash_internal
    ```

    ```console
    $ docker-compose exec elasticsearch bin/elasticsearch-reset-password --batch --user kibana_system
    ```

    If the need for it arises (e.g. if you want to [collect monitoring information][ls-monitoring] through Beats and
    other components), feel free to repeat this operation at any time for the rest of the [built-in
    users][builtin-users].

1. Replace usernames and passwords in configuration files

    Replace the password of the `elastic` user inside the `.env` file with the password generated in the previous step.
    Its value isn't used by any core component, but [extensions](#how-to-enable-the-provided-extensions) use it to
    connect to Elasticsearch.

    *:information_source: In case you don't plan on using any of the provided
    [extensions](#how-to-enable-the-provided-extensions), or prefer to create your own roles and users to authenticate
    these services, it is safe to remove the `ELASTIC_PASSWORD` entry from the `.env` file altogether after the stack
    has been initialized.*

    Replace the password of the `logstash_internal` user inside the `.env` file with the password generated in the
    previous step. Its value is referenced inside the Logstash pipeline file (`logstash/pipeline/logstash.conf`).

    Replace the password of the `kibana_system` user inside the `.env` file with the password generated in the previous
    step. Its value is referenced inside the Kibana configuration file (`kibana/config/kibana.yml`).

    See the [Configuration](#configuration) section below for more information about these configuration files.

1. Restart Logstash and Kibana to re-connect to Elasticsearch using the new passwords

    ```console
    $ docker-compose up -d logstash kibana
    ```

*:information_source: Learn more about the security of the Elastic stack at [Secure the Elastic Stack][sec-cluster].*


### Cleanup

Elasticsearch data is persisted inside a volume by default.

In order to entirely shutdown the stack and remove all persisted data, use the following Docker Compose command:

```console
$ docker-compose down -v
```


## Configuration

*:information_source: Configuration is not dynamically reloaded, you will need to restart individual components after
any configuration change.*

### How to configure Elasticsearch

The Elasticsearch configuration is stored in [`elasticsearch/config/elasticsearch.yml`][config-es].

You can also specify the options you want to override by setting environment variables inside the Compose file:

```yml
elasticsearch:

  environment:
    network.host: _non_loopback_
    cluster.name: my-cluster
```

Please refer to the following documentation page for more details about how to configure Elasticsearch inside Docker
containers: [Install Elasticsearch with Docker][es-docker].

### How to configure Kibana

The Kibana default configuration is stored in [`kibana/config/kibana.yml`][config-kbn].

You can also specify the options you want to override by setting environment variables inside the Compose file:

```yml
kibana:

  environment:
    SERVER_NAME: kibana.example.org
```

Please refer to the following documentation page for more details about how to configure Kibana inside Docker
containers: [Install Kibana with Docker][kbn-docker].

### How to configure Logstash

The Logstash configuration is stored in [`logstash/config/logstash.yml`][config-ls].

You can also specify the options you want to override by setting environment variables inside the Compose file:

```yml
logstash:

  environment:
    LOG_LEVEL: debug
```

Please refer to the following documentation page for more details about how to configure Logstash inside Docker
containers: [Configuring Logstash for Docker][ls-docker].

### How to scale out the Elasticsearch cluster

Follow the instructions from the Wiki: [Scaling out Elasticsearch](https://github.com/deviantony/docker-elk/wiki/Elasticsearch-cluster)

### How to reset a password programmatically

If for any reason your are unable to use Kibana to change the password of your users (including [built-in
users][builtin-users]), you can use the Elasticsearch API instead and achieve the same result.

In the example below, we reset the password of the `elastic` user (notice "/user/elastic" in the URL):

```console
$ curl -XPOST -D- 'http://localhost:9200/_security/user/elastic/_password' \
    -H 'Content-Type: application/json' \
    -u elastic:<your current elastic password> \
    -d '{"password" : "<your new password>"}'
```

## Extensibility

### How to add plugins

To add plugins to any ELK component you have to:

1. Add a `RUN` statement to the corresponding `Dockerfile` (eg. `RUN logstash-plugin install logstash-filter-json`)
1. Add the associated plugin code configuration to the service configuration (eg. Logstash input/output)
1. Rebuild the images using the `docker-compose build` command

### How to enable the provided extensions

A few extensions are available inside the [`extensions`](extensions) directory. These extensions provide features which
are not part of the standard Elastic stack, but can be used to enrich it with extra integrations.

The documentation for these extensions is provided inside each individual subdirectory, on a per-extension basis. Some
of them require manual changes to the default ELK configuration.

## Going further

### Plugins and integrations

See the following Wiki pages:

* [External applications](https://github.com/deviantony/docker-elk/wiki/External-applications)
* [Popular integrations](https://github.com/deviantony/docker-elk/wiki/Popular-integrations)

[elk-stack]: https://www.elastic.co/what-is/elk-stack
[xpack]: https://www.elastic.co/what-is/open-x-pack
[paid-features]: https://www.elastic.co/subscriptions
[es-security]: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html
[trial-license]: https://www.elastic.co/guide/en/elasticsearch/reference/current/license-settings.html
[license-mngmt]: https://www.elastic.co/guide/en/kibana/current/managing-licenses.html
[license-apis]: https://www.elastic.co/guide/en/elasticsearch/reference/current/licensing-apis.html

[elastdocker]: https://github.com/sherifabdlnaby/elastdocker

[linux-postinstall]: https://docs.docker.com/install/linux/linux-postinstall/

[booststap-checks]: https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks.html
[es-sys-config]: https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html

[win-filesharing]: https://docs.docker.com/desktop/windows/#file-sharing
[mac-filesharing]: https://docs.docker.com/desktop/mac/#file-sharing

[builtin-users]: https://www.elastic.co/guide/en/elasticsearch/reference/current/built-in-users.html
[ls-monitoring]: https://www.elastic.co/guide/en/logstash/current/monitoring-with-metricbeat.html
[sec-cluster]: https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html

[connect-kibana]: https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html
[index-pattern]: https://www.elastic.co/guide/en/kibana/current/index-patterns.html

[config-es]: ./elasticsearch/config/elasticsearch.yml
[config-kbn]: ./kibana/config/kibana.yml
[config-ls]: ./logstash/config/logstash.yml

[es-docker]: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
[kbn-docker]: https://www.elastic.co/guide/en/kibana/current/docker.html
[ls-docker]: https://www.elastic.co/guide/en/logstash/current/docker-config.html

[upgrade]: https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html
