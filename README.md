# CV Assignment 1
<p class="text-right">612410031 吳秉叡</p>

### Enviroment:
python 3.9
Windows 10

### third-party-package
Numpy
### Execute command
```python projection.py```

## Method description

First, I put my 2D and 3D data in **'points2D.txt'** and **'points3D.txt'**.

For Projection matrix in Q1, I calculate the matrix **A** below, which **X,Y,Z** are for 3D points and **x,y** are for 2D points.
Since we need to find **$min_{p\in R^{12}} P^TA^TAP$**, that is the minimal eigenvalue of $A^TA$.
![1.PNG](https://hackmd.io/_uploads/Sk01OKUQT.png)
Then use ```np.linalg.eig(np.matmul(A.T,A))``` to find the eigenvalue and eigenvector.
After all, we need to find the smallest eigenvalue by ```np.argmin(eigen_val)``` which corresponding to  the eigenvector that is called matrix **P**.

Then reshape it from dimension(12,1) to (3,4).

For $K,R,T$ matrice, them correspond to **calibration matrix**, **rotation matrix**  and **translation matrix**.

From the below formula, we get matrix $M$ from $P$, then we know $M^{-1}=QR$, which can calculate $K=R^{-1} , R=Q^{-1}$ , by using ```np.linalg.qr(M_inv)```to get $QR$, **M_inv** is for $M^{-1}$, then transform the into inverse matrix with ```np.linalg.inv()```.
![2.PNG](https://hackmd.io/_uploads/rk7CntL7p.png)
And for T, we know $T = K^{-1}P_4$ from below, $P_4$ is the fourth column of matrix $P$, then we cen get $T$ easily. 

![3.PNG](https://hackmd.io/_uploads/H17AhFUXp.png)


Finally, we calculate the average projection error from below formula.
![4.PNG](https://hackmd.io/_uploads/rkd3x9ImT.png)

The matrix $PX$ is 3D data matrix multiplcation with projection matrix, then we use ```np.sum()``` to sum all error value up, and divide it by ```np.size(PX,1)``` as the column number of $PX$.


## Experimental results

This is the final result in the terminal, and the matrix results are also save in **K.csv, P.csv, R.csv, T.csv** 
![5.PNG](https://hackmd.io/_uploads/H1MLQcIXT.png)


## Discussion of results

I've also tried another method that is to use ```np.linalg.svd``` to get the answer, and I found that $SVD$ matrix's principle is the same as the original method.

And calculate the answer with formula is the same as the format as not using python, such as the upper triangular matrix.

## Problems or difficulties you have encountered

At the beginning, I hadn't mentioned that the $PX$ matrix need to devide the homography part, so I always got very high error value like 500, but finally I solve it by the slide.
