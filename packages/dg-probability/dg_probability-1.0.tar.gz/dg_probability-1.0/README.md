# **Gaussian and Binomial Distributions**
This package contains code to perform basic mathematical operations on Gaussian and Binomial distributions. Operations include finding the mean and standard deviation (of both sample and population), plotting histograms for Gaussian distribution and plotting frequncy bar charts for Binomial distributions.

## Dummy input data
For Gaussian distribution, you can test the package using the following dummy input data.

```text
1
3
99
100
120
32
330
23
76
44
31
```

Here's some dummy data for a Binomial distribution. It contains the outcomes of 13 trials. A '0' denotes failure and a '1' denotes success.

```text
0
1
1
1
1
1
0
1
0
1
0
1
0
```

## Test the code
Copy the following code snippet in a `.py` file and execute it.

```python
from dg_probability import Gaussian

gaussian = Gaussian(10,5)
print(f"Gaussian mean = {gaussian.mean}")
print(f"Gaussian standard deviation = {gaussian.stdev}")
```

This snippet is for the Binomial module.

```python
from dg_probability import Binomial

binomial = Binomial(0.25,60)
print(f"Binomian mean = {binomial.mean}")
print(f"Binomian standard deviation = {binomial.stdev}")
```

# Test the entire Binomial distribution module
Here's how you can test the entire Binomial distribution module using the dummy data shown in the 'Input data' section. Create a file called `data_binomial.txt` and add the dummy data for Binomial distribution to it. Save this file in the same directory where your code is.

```python
# ignore if module is already imported
from dg_probability import Binomial

binomial = Binomial()
binomial.read_data_file('data_binomial.txt')
binomial.calculate_mean()
binomial.calculate_stdev()
binomial.replace_stats_with_data()
binomial.plot_bar()
binomial.plot_bar_pdf()
```

The methods for Gaussian distribution are similar.

## Contributions
There is not `CONTRIBUTIONS.md` file yet but you are welcome to create PRs :)

### Source code
https://github.com/dg1223/object-oriented-programming/tree/main/upload_to_pypi
