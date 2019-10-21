## OpenGL - Concepts Through Python

### Introduction

Following the article by [Muhammad Junaid Khalid](https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/) , where basic OpenGL concepts and setup was explained, now we'll be looking at how to make more **complex** objects and how to **animate** them.

OpenGL is very old, and you won't find many tutorials online on how to properly use it and understand it because all the top dogs are already knee-deep in new technologies. To understand modern OpenGL code, you have to first fully understand the bare-bones **ancient** concepts that were written on stone tablets by the wise Mayan game developers.

In this article, the following topics will be touched upon:

- [Basic Matrix Operations](#basicmatrixoperations)
- [Composite Transformations](#compositetransformations)
- [Transformations That Involve a Referral Point](#transformationsthatinvolveareferralpoint)
- [Initializing a Project Using PyGame](#initializingaprojectusingpygame)
- [Drawing Objects](#drawingobjects)
- [Iterative Animation](#iterativeanimation)
- [Implementation Example](#implementationexample)
- [Conclusion](#conclusion)



### Basic Matrix Operations 

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
> The exclamation point in conjunction with the exists symbol means: **A unique element E exists which...**

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



>I'll be explaining every single one of these transformations for the purpose of fully comprehending what is going on behind the scenes in OpenGL. But if you so desire, you can skip to the implementation itself.



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

Translation is implemented with the following OpenGL function:

```python
void glTranslatef(GLfloat tx,GLfloat ty,GLfloat tz);
```

As you can see, if we know the form of the Translation matrix, understanding the OpenGL function is very straightforward, this is the case with all OpenGL transformations.

> Don't mind the GLfloat is just a clever method for OpenGL to work on multiple platforms, you can look at it like this:
>
> ```C
> typedef float GLfloat;
> typedef double GLdouble;
> typedef someType GLsomeType;
> ```
>
> This is a necessary measure because not all systems have the same storage space for a `Char` for example.



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



3D rotation is implemented with the following OpenGL function:

```python
void glRotatef(GLfloat angle,GLfloat x,GLfloat y,GLfloat z);
```

- `angle` angle of rotation in degrees (0-360)
- `x,y,z` - vector around which the rotation is executed

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

```
void glScalef(GLfloat sx,GLfloat sy,GLfloat sz);
```



### Composite Transformations

Composite transformations are transformations which consist of more than 1 basic transformations (the ones listed above). Transformations `A` and `B` are combined by matrix multiplying the corresponding transformation matrices  `M_a` and `M_b`. 

This may seem like very straightforward logic, however there are some things that can be confusing. For example:

1. **Matrix multiplication is not commutable** , which means:
   $$
   A*B\neq B*A ~\\ \text{A and B being matrices}
   $$

2. Every single one of these transformations has an inverse transformation. An inverse transformation is a transformation that cancels out the original one. For example:

	$$
	T=\begin{bmatrix}
     1 & 0 & 0 &a\\
     0 & 1 & 0 &b\\
     0 & 0 & 1 &c\\
     0 & 0 & 0 &1\\
	\end{bmatrix}
	T^{-1}=\begin{bmatrix}
	  1 & 0 & 0 &-a\\
	  0 & 1 & 0 &-b\\
	  0 & 0 & 1 &-c\\
	  0 & 0 & 0 &1\\
	\end{bmatrix}
	E=\begin{bmatrix}
	  1 & 0 & 0 &0\\
	  0 & 1 & 0 &0\\
	  0 & 0 & 1 &0\\
	  0 & 0 & 0 &1\\
	\end{bmatrix}
	~\\ ~\\T*T^{-1}=E
	$$

3. When we want to make an inverse of a composite transformation, we have to change the order of elements utilized. 
   $$
   (A*B*C)^{-1} = C^{-1}*B^{-1}*A^{-1}
   $$
   
>You can look at it like this. The topological order of matrix utilization is very important, just like ascending to a certain floor of a building. If you're on the first floor, and you want to get to the fourth floor, first you need to go to the third floor and then to the fourth. But if you want to descend BACK to the second floor, you would then have to go to the third floor and then to the second floor (in reverse topological order).



### Transformations That Involve a Referral Point

As previously mentioned, when a transformation has to be done relative to a specific point in space, for example rotating around a referral point `A=(a,b,c)` in 3D space, not the origin `O = (0,0,0)`, we need to turn that referral point `A` into `O` by translating everything by `T(-a,-b,-c)`. Then we can do any transformation we need to do, and when we're done, translate everything back by `T(a,b,c)`, so that the original origin `O` again has the coordinates `(0,0,0)`. 

The matrix form of this example is:

$$
T*M*T^{-1}=\begin{bmatrix}
     1 & 0 & 0 & -a\\
     0 & 1 & 0 &-b\\
     0& 0 & 1 &-c\\
     0& 0 & 0 & 1\\
\end{bmatrix} 
*M*
\begin{bmatrix}
     1 & 0 & 0 & a\\
     0 & 1 & 0 & b\\
     0& 0 & 1 & c\\
     0& 0 & 0 & 1\\
\end{bmatrix}
$$
Where `M` is the transformation we wish to do on an object.

The whole point to learning these matrix operations is so that you can fully understand how OpenGL works, more on that later.

### Initializing a Project Using PyGame

First off, we need to install PyGame using pip. To do so run the following command:

```bash
python3 -m pip install -U pygame --user
```

If you have problems concerning the installation, go to this [webpage]( https://www.pygame.org/wiki/GettingStarted ).

Now finally, some actual code! 

Because I don't want to unload 3 books worth of Graphics theory on you, we'll be using the PyGame library. It will essentially just shorten the process from project initialization to actual modeling and animating.

To start off, we need to import everything necessary from both OpenGL and PyGame:

```python
import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
```



Next, we get to the initialization:

```python
pg.init() # initialization of all the pygame modules - this function is a godsend
windowSize = (1920,1080) # we define a fixed window size (4K is necessary of course)
pg.display.set_mode(display, DOUBLEBUF|OPENGL) # with this command we are specifying that we'll be using opengl with double buffering
# double buffering means that there are 2 images at any given time, one that we can see and one that we can transform as we see fit, we get to see the actual change caused by the transformations when the two buffers swap
```



Since we have our viewport set up, next we need to specify what we'll be seeing, or rather where the **camera** will be placed, and how far and wide it can see. This is know as the **frustum**, which is just a cut off pyramid that visually represents the camera's sight (what it can and can't see). Y'all gamers are probably very familiar with most of these terms, a **frustum** is defined by 4 key parameters:

1. The FOV (field of view) angle in degrees
2. The Aspect Ratio - which is defined as the ratio of the width and height
3. The z coordinate of the near Clipping Plane, which is the **minimum draw distance**
4. The z coordinate of the far Clipping Plane, which is the **maximum draw distance** 

The function itself and our implementation go as follows:

```c
void gluPerspective( GLdouble fovy,GLdouble aspect,GLdouble zNear,GLdouble zFar);
gluPerspective(60, (display[0]/display[1]), 0.1, 100.0)
```

To better understand how a frustum works, here's a reference picture:

![](C:\Users\vladimir\Desktop\OpenGL_AI\1200px-ViewFrustum.svg.png)



Near and far planes are used for better performance. Realistically, rendering anything outside our field of vision is a waste of hardware performance that could be used rendering something that we can actually see. So everything that the player can't see is implicitly stored in memory, even though it isn't visually present. If you still don't get how a frustum works, check out [this video](https://www.youtube.com/watch?v=VqH8kcmD-HI).

### Drawing Objects

After all this setup, I imagine we're asking ourselves the same question:

> Well this is all fine and dandy, but how do I make a Super Star Destroyer?

Well... **WITH DOTS**. Every model in OpenGL object is stored as a set of vertices and a set of their relations (which vertices are connected). So theoretically if you knew the position of every single dot that is used to draw a Super Star Destroyer, you could very well draw one!

There are a few ways we can model objects in OpenGL:

1. Drawing using vertices, and depending on how OpenGL interprets these vertices, we can draw with:
   - **points** (as in literal points that are not connected in any way)
   - **lines** (every pair of vertices constructs a connected line)
   - **triangles** (every 3 vertices make a triangle)
   - **quadrilateral** (every 4 vertices make a *mythical mathematical object of awesome power*, also known as a quadrilateral)
   - **polygon** 
   - **many more**
2. Drawing using the built in shapes and objects that were painstakingly modeled by OpenGL wizards
3. Importing fully modeled objects

So, to draw a cube for example, we first need to define it's vertices:

```python
cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1, -1, 1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1, -1))
```

![](D:\StackAbuse\openGL_series\openGL\Cube.png)



Then, we need to define how they're all connected. If we want to make a wire cube, we need to define the cube's edges:

```python
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
```



And if we want to make a solid cube, then we need to define the cube's quadrilaterals:

```python
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
```



> Keep in mind there's an actual reason we label the vertices as indexes of the array they're defined in. This makes writing code that connects them very easy.



The following function is used to draw a wired cube:

```python
def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()
```

`glBegin()` is a function that indicates we'll defining the vertices of a primitive in the code below. When we're done defining the primitive, we use the function `glEnd()`.

`GL_LINES` is a macro that indicates we'll be drawing lines.

`glVertex3fv`() - is a function that defines a vertex in space, there are a few versions of this function, so for the sake of clarity let's look at how the name is constructed:

- `glVertex` - a function that defines a vertex
- `glVertex3` - a function that defines a vertex using 3 coordinates
- `glVertex3f` - a function that defines a vertex using 3 coordinates of type GLfloat
- `glVertex3fv` - a function that defines a vertex using 3 coordinates of type GLfloat which are put inside a vector (tuple) (the alternative would be `glVertex3fl` which uses a list of arguments instead of a vector)



Following similar logic, the following function is used to draw a solid cube:

```python
def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()
```



### Iterative Animation

For our program to be **killable** we need to insert the following code snippet:

```python
for event in pg.event.get():
	if event.type == pg.QUIT:
        pg.quit()
        quit()
```

It's basically just a listener that scrolls through PyGame's events, and if it detects that we clicked kill window button, it quits the application. More on PyGame events in the following articles (I had to introduce this one right away because it would be quite uncomfortable for users and yourselves to have to fire up the task manager every time they want to quit the application).



In this example we'll be using double buffering, which just means that we'll be using two buffers (you can think of them as canvases for drawing) which will swap in fixed intervals and give the illusion of motion. Knowing this our code has to have the following pattern:

```python
handleEvents()
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
doTransformationsAndDrawing()
pg.display.flip()
pg.time.wait(1)
```

- `glClear` - a function that clears the specified buffers (canvases), in this case the color buffer (which contains color information for drawing the generated objects) and depth buffer (a buffer which stores in-front-of or in-back-of relations of all the generated objects). 

- `pg.display.flip()` - a function that updated the window with the active buffer contents

- `pg.time.wait(1)` - a function that pauses the program for a period of time

`glClear` has to be used because if we don't use it, we'll be just painting over an already painted canvas, which in this case is our screen.

Next, if we want to **continuously update our screen**, just like an animation, we have to put all our code inside a `while` loop in which we:

1. Handle events (in this case just quitting)
2. Clear the color and depth buffers co that they can be `drawn on` again
3. Transform and draw objects
4. Update the screen
5. GOTO 1.

The code ought to look something like this:

```python
while True:
    handleEvents()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    doTransformationsAndDrawing()
    pg.display.flip()
    pg.time.wait(1)
```



### Implementation Example

The code below draws a solid cube on the screen and continuously rotates it by 1 degree around the (1,1,1) vector. And it can be very easily modified to draw a wire cube.

```python
import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1, -1, 1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1, -1))
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))


def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()
def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def main():
    pg.init()
    display = (1680,1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        solidCube()
        #wireCube()
        pg.display.flip()
        pg.time.wait(10)
   
if __name__ == "__main__":
    main()
```



### Conclusion

There is a **LOT** more to learn about OpenGL, like lighting, textures, advanced surface modeling, composite modular animation and much more. But fret not, all of this will be explained in the following articles. I'm here to teach the public about OpenGL the proper way, from the ground up. 

And don't worry, in the article we'll actually draw something semi decent.