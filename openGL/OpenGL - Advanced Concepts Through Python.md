## OpenGL - Advanced Concepts Through Python

### Introduction

Following the well-written article by [Muhammad Junaid Khalid](https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/) , where basic OpenGL concepts and setup was explained, now we'll be looking at how to make more **complex** objects and how to **animate** them.

In this article, the following topics will be touched upon:

- Geometry Background
- Basic OpenGL Transformations
- Project Preparation
- Camera Setup
- Modeling Complex Objects
- Animation
- Conclusion



### Geometry Background

To understand what's happening with all these glTranslate's and whatnot, we'll first need to learn a little bit of geometry.

Every single **point in space** can be represented with **Cartesian coordinates**. Coordinates represent any given point's location by defining it's **X**, **Y** and **Z** values. We'll be practically using them as **1x3 matrices**, or rather 3-dimensional **vectors** (more on matrices later on). Examples of some coordinates:
$$
a =(5,3,4)~\\b=(9,1,2)
$$
`a` and `b` being points in space, their x-coordinates being 5 and 9 respectively, y-coordinates being 3 and 1 and so on.

In computer graphics, more often than not, **homogeneous** coordinates are utilized instead of regular old **Cartesian coordinates**, they're basically the same thing, only with an additional utility parameter, which for the sake of simplicity we'll say is always 1. So if the regular coordinates of `a` are `(5,3,4)`,  the corresponding homogeneous coordinates would be `(5,3,4,1)`. There's a lot of geometric theory behind this, but it isn't really necessary for this article, if you're interested in the cold hard math theory.

Next, an essential tool for representing geometric transformations are **matrices**. A matrix i basically a two-dimensional array (in this case of size **n*****n**, it's very important for them to have the same number of rows and columns). Now, matrix operations are more often than not, pretty straightforward, like addition, subtraction etc. But of course the most important operation has to be the most complicated one, multiplication. Let's take a look at basic matrix operation examples:
$$
A = \begin{bmatrix}
     1 & 2 & 5 \\
     6 & 1 & 9 \\
     5& 5 & 2 \\
\end{bmatrix} - \text{Example matrix}~\\
\begin{bmatrix}
     1 & 2 & 5 \\
     6 & 1 & 9 \\
     5& 5 & 2 \\
\end{bmatrix} +
\begin{bmatrix}
     2 & 5 & 10 \\
     12 & 2 & 18 \\
     10 & 10 & 4 \\
\end{bmatrix} =
\begin{bmatrix}
     3 & 7 & 15 \\
     18 & 3 & 27 \\
     15 & 15 & 6 \\
\end{bmatrix} - \text{Matrix addition}~\\
\begin{bmatrix}
     2 & 4 & 10 \\
     12 & 2 & 18 \\
     10 & 10 & 4 \\
\end{bmatrix}-
\begin{bmatrix}
     1 & 2 & 5 \\
     6 & 1 & 9 \\
     5& 5 & 2 \\
\end{bmatrix}
 =
\begin{bmatrix}
    1 & 2 & 5 \\
     6 & 1 & 9 \\
     5& 5 & 2 \\
\end{bmatrix} - \text{Matrix subtraction}~\\
$$


Now, as all math tends to do, it gets relatively complicated when you actually want something practical out of it. The formula for matrix multiplication goes as follows:
$$
c[i,j] =  \sum_{k=1}^{n}a[i,k]*b[k,j]
$$
`c` being the resulting matrix, `a` and `b` being the multiplicand and the multiplier. 

OK, before you start running, there's a simple explanation for this formula. Every element can be constructed by summing the products of all the elements in the `i`-th row and the `j`-th column. This is the reason why in `a[i,k]`, the `i` is fixed and the `k` is used to iterate through the elements of the corresponding row. Same principle can be applied to `b[k,j]`. 

Knowing this, there's an additional condition that needs to be fulfilled for us to be able to use matrix multiplication. If we want to multiply matrices `A` and `B` of dimensions `a*b` and `c*d` . The number of elements in a single row in the first matrix (`b`) has to be the same as the number of elements in a column in the second matrix (`c`), so that the formula above can be used properly.

A very good way of visualizing this concept is highlighting the rows and columns who's elements are going to be utilized in the multiplication for a given element. Image the two highlighted **lines**  over each other, as if they're in the same matrix. The element where they intercept is the position of the resulting element of the summation of their products.

Matrix multiplication is so important because if we want to explain the following expression in simple terms: `A*B` (A and B being matrices), we would say: `we are transforming A using B`. This is why matrix multiplication is the quintessential tool for transforming any object in OpenGL or geometry in general.

The last thing you need to know about matrix multiplication is that it has a **neutral**, which means there is a unique element (matrix in this case) `E` which when multiplied with any other element `A` doesn't change `A`'s value, that is:
$$
(!\exists{E}\ \ \forall{A})\ E*A=A
$$
The exclamation point in conjunction with the exists symbol means: **A unique element E exits which...**

In case of multiplication with normal integers, `E` has the value of `1`. In case of matrices, E has the following values in normal **Cartesian** (`E_1`) and **homogeneous coordinates** (`E_2`)  respectively:
$$
E_1=\begin{bmatrix}
     1 & 0 & 0 \\
     0 & 1 & 0 \\
     0& 0 & 1 \\
\end{bmatrix}
E_2=\begin{bmatrix}
     1 & 0 & 0 & 0\\
     0 & 1 & 0 &0\\
     0& 0 & 1 &0\\
     0& 0 & 0 & 1\\
\end{bmatrix}
$$


Every single geometric transformation has it's own unique transformation matrix that has a pattern of some sort, of which the most important are:

1. Translation
2. Scaling
3. Reflection
4. Rotation
5. Sheering

>I'll be explaining every single one of these transformations for the sake of fully comprehending what is going on behind the scenes in OpenGL. But if you so desire, you can skip to the implementations themselves.



#### Translation

Translation is the act of literally moving an object by a set vector, the object that's affected by the transformation doesn't change it's shape in any way, nor does it change it's orientation, it's just moved in space (that's why translation is classified as a **movement** transformation). 

Translation can be described with the following matrix form:


$$
T=\begin{bmatrix}
     1 & 0 & 0 & t_x\\
     0 & 1 & 0 &t_y\\
     0& 0 & 1 &t_z\\
     0& 0 & 0 & 1\\
\end{bmatrix}
$$

The `t`-s represents by how much the object's `x`,`y` and `z` location values will be changed.

So, after we transform any coordinates with the translation matrix`T` we get:
$$
[x,y,z]*T=[t_x+x,t_y+y,t_z+z]
$$


#### Rotation

Rotation is bit more complicated transformation, because of the simple fact it's dependent on 2 factors:

1. Around what line  in 3D space(or point in 2D space) we'll be rotating
2. By how much (in degrees or radians) we'll be rotating

Because of this, we first need to define rotation in a 2D space, and for that we need a bit of trigonometry. 

Here's a quick reference:

![](C:\Users\vladimir\Desktop\OpenGL_AI\trougao_opengl.png)



> These trigonometric functions can only be used inside a right-angled triangle (one of the angles has to be 90 degrees).

The base rotation matrix for rotating an object in 2D space around the vertex (0,0) by the angle `A` goes as follows:
$$
\begin{bmatrix}
     cosA & -sinA & 0\\
     sinA & cosA  & 0\\
     0 & 0  & 1\\
    
\end{bmatrix}
$$


> Again, the 3rd row and 3rd column are just in case we want to stack translation transformations on top of other transformations (which we will in OpenGL), it's ok if you don't fully grasp why they're there, things should clear up in the composite transformation example.



This was all in 2D space, now let's move on to 3D space. In 3D space we need to define a matrix that can rotate an object around **any** line. As a wise man once said: `Keep it simple and stupid!` Fortunately, math magicians did for once keep it simple and stupid. 

Every single rotation around a line can be broken down into 3 different transformations:

1. Rotation around the x axis
2. Rotation around the y axis
3. Rotation around the z axis
4. Utility translations (which will be touched upon later)

So, the only three things we need to construct any 3D rotation are matrices that represent rotation around the `x`,`y` and `z` axis by an angle `A`:
$$
R_x=\begin{bmatrix}
     1 & 0 & 0 & 0\\
     0 & cosA & -sinA &0\\
     0& sinA & cosA &0\\
     0& 0 & 0 & 1\\
\end{bmatrix}
R_y=\begin{bmatrix}
     cosA & 0 & sinA & 0\\
     0 & 1 & 0 &0\\
     -sinA& 0 & cosA &0\\
     0& 0 & 0 & 1\\
\end{bmatrix}
R_z=\begin{bmatrix}
     cosA & -sinA & 0 & 0\\
     sinA & cosA & 0 &0\\
     0& 0 & 1 &0\\
     0& 0 & 0 & 1\\
\end{bmatrix}
$$


#### Scaling

Scaling is the act of multiplying any dimension of the target object by a **scalar**, this scalar can be `<1` if we want to shrink the object, and it can be `>1` if we want to enlarge the object.

Scaling can be described with the following matrix form:
$$
S=\begin{bmatrix}
     s_x & 0 & 0 & 0\\
     0 & s_y & 0 &0\\
     0& 0 & s_z &0\\
     0& 0 & 0 & 1\\
\end{bmatrix}
$$
`s_x`, `s_y`,`s_z` are the scalars that are multiplied with the `x`, `y` and `z` values of the target object. 

After we transform any coordinates with the scaling matrix`S` we get:
$$
[x,y,z]*S=[s_x*x,s_y*y,s_z*z]
$$

This transformation is particularly useful when scaling an object by factor `k` (this means the resulting object is two times bigger), this is achieve this by setting `s_x`=`s_y`=`s_z`=`k`.
$$
[x,y,z]*S=[s_x*x,s_y*y,s_z*z]
$$

A special case of scaling is known as `reflection`, and it's achieved by setting either `s_x`,`s_y` or `s_z` to `-1`. This just means we invert the sign of one of the object's coordinates, in simpler terms, we **put the object on the other side of the x,y or z axis**, this transformation can be modified to work for any plain of reflection, but we don't really need it for now.



