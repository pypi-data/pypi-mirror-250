# Confboy

Better configs with TOML support.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install confboy.

```bash
pip install confboy
```

## Usage

```python
import confboy


base_config = {
    'nested': {
        'one': 1,
        'two': 2,
    },
    'three': 3,
}

config = confboy.Config(base_config)

config.nested.one  # Returns `1`
config.three       # Returns `3`
```

Although it is advised not to change the config
during runtime, it is also possible:

```python
config.nested.one = 10
config.nested.one  # Returns `10`

config.new_nested = {'one': 1}
config.new_nested.one  # Returns `10`
```

Confboy also supports dynamic values
that can use other values from the same config.
You can use it to build connection URLs or whatever.
Shines with changing config during runtime:
change `config.postgres.user` and `config.postgres.url`
will be rebuilt on every query if it's a callable.
You can do various things with it including mapping
and filtering values the app got from the TOML config,
cast types, whatever comes to your mind.
Callables work on any nested level.

```python
config = confboy.Config({
    'a': {'a': 1},
    'b': 2,
    'a_plus_b': 'callable:add',  # Tell confboy to call `add` from provided callables
})


def add():
    return config.a.a + config.b


config.register_callable(add)
config.a_plus_b  # Returns 3
```

Confboy can take values from TOML files as well.
Provided config will be merged over base config.

```toml
# config.toml

[nested]
one = 1
two = 2

not = "nested"
```

```python
config = confboy.Config(toml_config_path='config.toml')
config.nested.one  # Returns 1
config.not         # Returns 'nested'
```

Confboy's merges are __soft__: if the value
is present in the config but not in patch,
it won't be deleted from the config.
It supports value deletion and everything.
Just try it out or check the source code!


## Async functions as callables

Currently `confboy` does not support asynchronous functions
as callables. That would bring interface inconsistency
like `await config.foo` vs `config.foo`. You can wrap
your asynchronous function like that:

```python
config.register_callable(
    functools.partial(asyncio.run, async_func()))
```

Although that'd block the event loop.


