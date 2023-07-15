# DOPBO
Drainable One-Pot Bayesian Optimization

This code is for a ternary mixture.

# Requirements
Python >= 3.7

# Usage

## Parameters

**drainage_index: int** (parameter determining the maximum amount for drainage)

**delta: int** (minimum unit of injection amounts)

**add_max: float** (parameter determining the maximum amount for injection)


## Target dataset

The target dataset is prepared as data.csv.

The example is as follows.

|  objective  |  amount1  |  amount2 |  amount3 |
| ------ | ------------ | ------------ |
|  5  |  1  | 0  | 0  |
|  2  |  0  | 1  | 0  |
|  4  |  0  | 0  | 1  |

The final row indicates the present objective function value and amounts of liquid samples.


## Execution
```
python DOPBO.py 
```

# License
This project is licensed under the terms of the MIT license.
