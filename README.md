# Coolab
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
[![PyPI version](https://badge.fury.io/py/coolab.svg)](https://badge.fury.io/py/coolab)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)

*Instantly working cool apps you can use on Google Colab In ONE line!*

## Available Apps

#### 1. vscode

```import coolab; coolab.Code().run()```

#### 2. more to come

## How to Use in Google Colab?


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1SyUpFRWQrgriUnJcLGMatDvxxKP9TU5r?usp=sharing)

```
!pip install coolab # install package using pip
import coolab; coolab.Code().run() # run in seconds.
```

## How Fast is it

We cache vscode installation files and configurations in your google drive if you choose to mount your drive. It takes much less time if you run the same code at the second time.

* VScode installation package is cached (so need to re-download vscode)
* Your connection token is cached (never worry about configuration)
* Working directory is cached (so you always automatically get directed back to the last working directory)

## Next Step

We aim to provide more online tools using the computation resource of Google Colab. You start to use these awesome tools and we deal with the rest!

## Suggestions

Feel free to create new [issue](https://github.com/songlinhou/coolab/issues) so we can improve this library!