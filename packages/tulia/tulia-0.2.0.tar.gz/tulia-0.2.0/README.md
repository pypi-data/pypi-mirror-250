<div align="center">

![logo](/docs/logo.png)

Tulia: a comprehensive machine learning project entirely from scratch, utilizing the power of Python and numpy.

</div>

## Features

### Simplicity

By encapsulating both the training and predicting logic within just a couple of classes, complexity is greatly reduced compared to popular frameworks that heavily rely on abstraction.
Moreover, the library provided here offers a streamlined approach by maintaining only essential parameters in the model class. 

### Familiar approach

This library uses sklearn API to build the codebase. 

## Example usage

```python
from src.linear import LinearRegression

X_train, X_test, y_train, y_test = ...

lr = LinearRegression(n_steps=10_000, learning_rate=1e-4)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)

mse = mean_squared_error(y_pred, y_test)  # Here mean_squared_error() is a pseudocode.
```

## Installation


### To use in code

```sh
pip install scratch-ml
```

### Download a whole library

```sh
git clone https://github.com/chuvalniy/Torchy.git
pip install -r requirements.txt
```

## Testing

Every machine learning model is provided with unit test that verify correctness of fit and predict methods.

Execute the following command in your project directory to run the tests.

```python
pytest -v
```

## License
MIT License
