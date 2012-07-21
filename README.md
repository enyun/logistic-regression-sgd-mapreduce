logistic-regression-sgd-mapreduce
=================================

# Overview
Python scripts for building binary classifiers using logistic regression with stochastic gradient descent, packaged for use with map-reduce platforms supporting Hadoop streaming.

# ￼Algorithm
* Distributed regularized binary logistic regression with stochastic gradient descent [[1]], [[2]]
	* Competitive with best extant large-scale supervised learning algorithms
	* Results provide direct estimation of probability of class membership 
* Implementation supports large-scale learning using Hadoop streaming


    $ cd logistic-regression-sgd-mapreduce

# Data formats

## Instances
    <instance> ::= { "class": <class>, "features": { <feature>: <value>, … , <feature>: <value> } }
    <class>    ::= 0 | 1
    <feature>  ::= a JSON string
    <value>    ::= a JSON float in the interval [0.0, 1.0]   

## Models
    <model> ::= { <feature>: <weight>, … , <feature>: <weight> }
    <weight> ::= a JSON float in the interval [0.0, 1.0]

## Confusion matrices
    <confusion_matrix> ::= { "TP": <count>, "FP": <count>, "FN": <count>, "TN": <count> }
    <count>            ::= a JSON int in the interval [0, inf)
    
# Usage

## From a UNIX shell

### Convert data in SVMLight format into instances
Convert a file with data in SVM<sup><i>Light</i></sup> [[8]] format into a file containing instances.

    $  cat train.data.svmlight | ./parse_svmlight_examples.py | awk 'BEGIN{srand();} {printf "%06d %s\n", rand()*1000000, $0;}' | sort -n | cut -c8- > train.data
    $  cat test.data.svmlight | ./parse_svmlight_examples.py | awk 'BEGIN{srand();} {printf "%06d %s\n", rand()*1000000, $0;}' | sort -n | cut -c8- > test.data

### Train a model
Generate a model from training data.

    $ cat train.data | ./train_map.py | sort | ./train_reduce.py > model

### Test a model
Generate a confusion matrix based on running a model against test data.

    $ cat test.data | ./test_map.py model | sort | ./test_reduce.py > confusion-matrix
    
### Predict
Generate a tab-separated file containing an instance preceded by a margin-based certainty based on the estimated probability of the instance, sorted in increasing order of certainty.

    $ cat test.data | ./predict_map.py model | sort | ./predict_reduce.py > predictions
    
## Using Elastic MapReduce
TBD
    
# References

[[1]] Cohen, W. Stochastic Gradient Descent. Downloaded from http://www.cs.cmu.edu/~wcohen/10-605/notes/sgd-notes.pdf. (2012).



[1]: http://www.cs.cmu.edu/~wcohen/10-605/notes/sgd-notes.pdf "Cohen, W. Stochastic Gradient Descent. Downloaded from http://www.cs.cmu.edu/~wcohen/10-605/notes/sgd-notes.pdf. (2012)."
[8]: http://svmlight.joachims.org/ "Joachims, T. SVM<sup><i>Light</i></sup> Support Vector Machine. Downloaded from http://svmlight.joachims.org/. (2008)."