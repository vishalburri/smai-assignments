"""
Course: Statistical Methods in Artificial Intelligence (CSE471)
Semester: Fall '17
Professor: Gandhi, Vineet

Assignment 2: Check if the 2D points are linearly separable and if they
are not, implement a kernel that maps them to 3-dimensional space
where they are linearly separable. We prove they are indeed linearly
separable using a perceptron linear classifier.
Skeleton code for visualizing 2D points and writing a kernel for mapping
them to a higher dimensional space. Use the perceptron given by sklearn and
prove that the kernel mapping makes the points linearly separable, using a
simple perceptron.
This is your final submission file.

Dataset is generated manually.

Remember
--------
"""

from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import argparse, os, sys

def get_input_data(filename):

    X = []; Y = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().split()
            Y.append(int(line[0]))
            X.append([float(x) for x in line[1:]])
    X = np.asarray(X); Y = np.asarray(Y)

    return X, Y

def calculate_accuracy(predictions, labels):

    return accuracy_score(labels, predictions)

def kernelize(X, Y):


    # YOUR CODE HERE
    ''' Initialize kernelX array'''
    kernelX = []

    for j in range(X.shape[0]):
      '''New  data is x1^2,x2^2,x1*x2 3-D Points'''
      data = [X[j][0]*X[j][0]]

      data = data + [X[j][0]*X[j][1]]

      data = data + [X[j][1]*X[j][1]]
      ''' add data to kernelX '''
      kernelX = kernelX + [data]
      ''' convert it into array '''
    kernelX = np.asarray(kernelX)

    """
    ===========================================================================
    """

    """
    Code to visualize the generated 3D data after applying the kernel function, so
    that it is easier to decide which kernel works.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color = lambda x: 'r' if x else 'b'
    mark = lambda x: 'o' if x else '^'
    for i in range(kernelX.shape[0]):
        x,y,z = kernelX[i]
        ax.scatter(x, y, z, c=color(Y[i]), marker=mark(Y[i]))
    plt.show()

    return kernelX

def perceptron(X, Y):


    is_linearly_separable = False
    kernelX = kernelize(X, Y)           # Y is passed to plot the kernelized data with labels

    """
    Create a Perceptron instance and fit it to the kernelized data.
    For details on how to do this in scikit-learn, refer:
        http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html
    ==========================================================================
    """

    # YOUR CODE GOES HERE
    ski = Perceptron(max_iter=11000)
    ski.fit(kernelX,Y)
    train_predictions = ski.predict(kernelX)
    train_labels = Y


    train_accuracy = calculate_accuracy(train_predictions, train_labels)
    print "Training Accuracy: %.4f" % (train_accuracy)

    if train_accuracy == 1:
        is_linearly_separable = True

    """
    Code to plot the 3D decision surface that separates the points. Visualization
    will help in understanding how the kernel has performed.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color = lambda x: 'r' if x else 'b'
    mark = lambda x: 'o' if x else '^'
    for i in range(kernelX.shape[0]):
        x, y, z = kernelX[i]
        ax.scatter(x, y, z, c=color(Y[i]), marker=mark(Y[i]))

    W = ski.coef_[0]                # 3D normal
    intercept = ski.intercept_[0]   # Distance from origin

    xx, yy = np.meshgrid(kernelX, Y)
    """
    Derived from a*x + b*y + c*z + d = 0. (a, b, c) is the normal and we know
    x and y values. d is the distance from origin, or the intercept. Hence, value
    of z => (-a*x - b*y - d) / c.
    Source: https://stackoverflow.com/questions/3461869/plot-a-plane-based-on-a-normal-vector-and-a-point-in-matlab-or-matplotlib
    """
    zz = ((-W[0] * xx) + (-W[1] * yy) + (-intercept)) * 1. / W[2]

    ax.plot_surface(xx, yy, zz, rstride=10, cstride=10, color='g', antialiased=False,
            linewidth=0, shade=False)
    plt.show()

    return is_linearly_separable


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', default=None,
            help='path to the directory containing the dataset file')

    args = parser.parse_args()
    if args.data_dir is None:
        print "Usage: python kernel_trick_perceptron.py --data_dir='<dataset dir path>'"
        sys.exit()
    else:
        filename = os.path.join(args.data_dir, 'linearly_inseparable.data')
        try:
            if os.path.exists(filename):
                print "Using %s as the dataset file" % filename
        except:
            print "%s not present in %s. Please enter the correct dataset directory" % (filename, args.data_dir)
            sys.exit()



    # YOUR CODE GOES HERE
    [X,Y] = get_input_data(filename)



    if(perceptron(X, Y)):
        print "Data is linearly separable using the current kernel."
    else:
        print "Data is still not linearly separable using the current kernel."