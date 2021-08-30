# PHT Internal services deployment

## Login to the gitlab container registry
```shell
docker login registry.gitlab.com
```

## Configure vault
Vault needs to be configured manually since secret information is created in memory.

1. Start vault with `docker-compose` 
    ```shell
    docker-compose up -d vault
    ```

2. Shell into the running container
    ```shell
    docker exec -it pht-vault sh
    ```
3. Initialize vault and note down the displayed unseal keys and root token.
    ```shell
    vault operator init
    ```

4. Vaul starts in a sealed state by default, unseal it by performing the unseal operation with three of the previously displayed keys
    ```shell
    vault operator unseal
    ```
   After sucecssfully unsealing the output should look something like this
    ```shell
    Key             Value
    ---             -----
    Seal Type       shamir
    Initialized     true
    Sealed          false
    Total Shares    5
    Threshold       3
    Version         1.8.2
    Storage Type    file
    Cluster Name    vault-cluster-f71e64c1
    Cluster ID      d579ca48-c925-c560-ae26-b0cd8b2693b6
    HA Enabled      false
    ```
5. Login with the root token generated in step 3
    ```shell
    vault login
    ```
6. Enable the secrets engines used by the PHT
    ```shell
    vault secrets enable -version=1 -path=services kv
    ```
    ```shell
    vault secrets enable -version=1 -path=station_pks kv 
    ```
    ```shell
    vault secrets enable -version=1 -path=user_pks kv
    ```
    ```shell
    vault secrets enable -version=2 -path=kv-pht-routes kv
    ```
   To check that all engines were create run `vault secrets list`


## .env file
Define environment variables used for multiple services in the `.env` file

## Running the rest of the services


## Installing vault


