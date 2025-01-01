# Dependencies

-   python3
-   docker
-   SSH

# Startup

After cloning the repository you will need to create the .venv:

```shell
python3 -m venv .venv
```

Install the package dependencies:

```shell
pip install .
```

And set the source:

```shell
source .venv/bin/activate
```

For testing you will need a container running with a ssh server, for this run:

```shell
docker compose up
```
