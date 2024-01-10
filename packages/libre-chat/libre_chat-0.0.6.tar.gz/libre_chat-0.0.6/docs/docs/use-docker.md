[![Image size](https://ghcr-badge.egpl.dev/vemonet/libre-chat/size)](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat)

Libre Chat is available as a [docker image](https://github.com/vemonet/libre-chat/pkgs/container/libre-chat), it is recommended to use docker for deploying in production as it uses gunicorn to run multiple workers.

!!! Warning "Shared memory for multiple users"

    Memory of the chatbot is shared betweem the users that are on the same worker.

## ⚡ Quickstart

If you just want deploy it using the pre-trained Mixtral model, you can use docker:

```bash
docker run -it -p 8000:8000 ghcr.io/vemonet/libre-chat:main
```

## ⚙️ Configure with docker compose

1. Create a `chat.yml` file with your chat web service configuration.
2. Create the `docker-compose.yml` in the same folder:

    ```yaml title="docker-compose.yml"
    version: "3"
    services:
      libre-chat:
        image: ghcr.io/vemonet/libre-chat:main
        volumes:
          # ⚠️ Share files from the current directory to the /data dir in the container
          - ./chat.yml:/data/chat.yml
          - ./models:/data/models
          - ./documents:/data/documents
          - ./embeddings:/data/embeddings
          - ./vectorstore:/data/vectorstore
        ports:
          - 8000:8000
        environment:
          - LIBRECHAT_WORKERS=1
    ```

3. Start your chat web service with:

    ```bash
    docker compose up
    ```

??? warning "Using multiple workers"

    Using multiple worker is still experimental. When using a documents-based QA chatbot you will need to restart the API after adding new documents to make sure all workers reload the newly built vectorstore.
