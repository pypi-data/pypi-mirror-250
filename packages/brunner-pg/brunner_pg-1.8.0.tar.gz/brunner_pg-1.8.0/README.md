# brunner

The postgres extension client for the [Brunner](https://windmill.dev) platform.

[windmill-api](https://pypi.org/project/windmill-api/).

## Quickstart

```python
import brunner_pg


def main():
    my_list = query("UPDATE demo SET value = 'value' RETURNING key, value")
    for key, value in my_list:
        ...
```
