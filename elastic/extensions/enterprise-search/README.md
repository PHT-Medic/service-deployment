# Enterprise Search extension

Elastic Enterprise Search is a suite of products for search applications backed by the Elastic Stack.

## Requirements

* 2 GB of free RAM, on top of the resources required by the other stack components and extensions.

Enterprise Search exposes the TCP port `3002` for its Web UI and API.

## Usage

### Generate an encryption key

Enterprise Search requires one or more [encryption keys][enterprisesearch-encryption] to be configured before the
initial startup. Failing to do so prevents the server from starting.

Recommended are 256-bit keys for optimal security.

Those encryption keys must be added manually to the [`config/enterprise-search.yml`][config-enterprisesearch] file. By
default, the list of encryption keys is empty and must be populated using one of the following formats:

```yaml
secret_management.encryption_keys:
  - my_first_encryption_key
  - my_second_encryption_key
  - ...
```

### Enable Elasticsearch's API key service

Enterprise Search requires Elasticsearch's built-in [API key service][es-security] to be enabled in order to start.
Unless Elasticsearch is configured to enable TLS on the HTTP interface (disabled by default), this service is disabled
by default.

To enable it, modify the Elasticsearch configuration file in [`elasticsearch/config/elasticsearch.yml`][config-es] and
add the following setting:

```yaml
xpack.security.authc.api_key.enabled: true
```

### Start the server

To include Enterprise Search in the stack, run the docker-compose.yml file from the root directory but comment out
the service for enterprise search.

Allow a few minutes for the stack to start, then open your web browser at the address <http://localhost:3002> to see the
Enterprise Search home page.

Enterprise Search is configured on first boot with the following default credentials:

* user: *enterprise_search*
* password: *changeme*

## Configuring Enterprise Search

Any change to the Enterprise Search configuration requires a restart of the Enterprise Search container:

```console
$ docker-compose -f docker-compose.yml -f extensions/enterprise-search/enterprise-search-compose.yml restart enterprise-search
```


## See also

[Enterprise Search documentation][enterprisesearch-docs]

[config-enterprisesearch]: ./config/enterprise-search.yml

[enterprisesearch-encryption]: https://www.elastic.co/guide/en/enterprise-search/current/encryption-keys.html
[enterprisesearch-security]: https://www.elastic.co/guide/en/workplace-search/current/workplace-search-security.html
[enterprisesearch-config]: https://www.elastic.co/guide/en/enterprise-search/current/configuration.html
[enterprisesearch-docker]: https://www.elastic.co/guide/en/enterprise-search/current/docker.html
[enterprisesearch-docs]: https://www.elastic.co/guide/en/enterprise-search/current/index.html
[enterprisesearch-ui]: https://www.elastic.co/guide/en/enterprise-search/current/user-interfaces.html

[es-security]: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#api-key-service-settings
[config-es]: ../../elasticsearch/config/elasticsearch.yml
[config-kbn]: ../../kibana/config/kibana.yml
