# 15/11/24 3D WireFrame Projector
# libraries
import turtle
import numpy as np




# takes input xyz, which if is a rotation represents the boolean value of which axis the object is being rotated parallel to
# if transformation is a dilation the x value will be whether it is enlarged (1) or shrunk (-1)
# if its a translation, it is the translation vector
# theta is only use if a rotation, it is the radians the object is rotated anticlockwise around the origin
# transform_type represents whether a translation, rotation or dilation

def transform_object(x,y,z,theta,transform_type):

    # access the vertices, object type (eg cube,cuboid) and size/scale of object
    global vertices, object_type, scale

    # check type of transformation
    if transform_type=="rotate":

        # if rotation then check if parallel to xyz axis

        if x==True:
            transform=np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])

        if y==True:
            transform=np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])
            
        if z==True:
            transform=np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
    
        vertices=np.dot(vertices,transform.T) # apply transformation to vertices

    # if translation, add translation vector to vertices

    if transform_type=="translate":
        transform=np.array([x,y,z
        ])
        vertices=vertices+transform
    
    # if dilation then scale object back to unit object, then dilate it by scale factor given
    if transform_type=="dilate":

        scaleFactor=x
         
        # scale must not <2 otherwise will delete object
        if not (x<0 and scale<2):
            vertices = vertices / scale
            scale+=scaleFactor
            vertices = vertices * scale
        
    

    # find objects edges between each vertex
    generateEdges()


def generateEdges():
    
    global vertices

    if object_type=="cube":
        edges = np.array([
            [vertices[0], vertices[1]],
            [vertices[1], vertices[2]],
            [vertices[2], vertices[3]],
            [vertices[3], vertices[0]],
            [vertices[4], vertices[5]],
            [vertices[5], vertices[6]],
            [vertices[6], vertices[7]],
            [vertices[7], vertices[4]],
            [vertices[0], vertices[4]],
            [vertices[1], vertices[5]],
            [vertices[2], vertices[6]],
            [vertices[3], vertices[7]]
        ])
    elif object_type=="cuboid":
        edges = np.array([
            [vertices[0], vertices[1]],  # Edge 0 to 1
            [vertices[0], vertices[2]],  # Edge 0 to 2
            [vertices[0], vertices[4]],  # Edge 0 to 4
            [vertices[1], vertices[3]],  # Edge 1 to 3
            [vertices[1], vertices[5]],  # Edge 1 to 5
            [vertices[2], vertices[3]],  # Edge 2 to 3
            [vertices[2], vertices[6]],  # Edge 2 to 6
            [vertices[3], vertices[7]],  # Edge 3 to 7
            [vertices[4], vertices[5]],  # Edge 4 to 5
            [vertices[4], vertices[6]],  # Edge 4 to 6
            [vertices[5], vertices[7]],  # Edge 5 to 7
            [vertices[6], vertices[7]]   # Edge 6 to 7
        ])
    elif object_type=="pyramid":
        edges = np.array([
            [vertices[0], vertices[1]],  # Edge 0 to 1 (Base)
            [vertices[1], vertices[3]],  # Edge 1 to 3 (Base)
            [vertices[3], vertices[2]],  # Edge 3 to 2 (Base)
            [vertices[2], vertices[0]],  # Edge 2 to 0 (Base)
            [vertices[0], vertices[4]],  # Edge 0 to 4 (Apex)
            [vertices[1], vertices[4]],  # Edge 1 to 4 (Apex)
            [vertices[2], vertices[4]],  # Edge 2 to 4 (Apex)
            [vertices[3], vertices[4]]
            ])
    
    elif object_type == "dodecahedron":
        edge_indices = [
            (0,8), (0,12), (0,16), (1,8), (1,13), (1,17),
            (2,9), (2,12), (2,18), (3,9), (3,13), (3,19),
            (4,10), (4,14), (4,16), (5,10), (5,15), (5,17),
            (6,11), (6,14), (6,18), (7,11), (7,15), (7,19),
            (8,9), (10,11), (12,14), (13,15), (16,17), (18,19)
        ]
        edges = np.array([[vertices[i], vertices[j]] for i, j in edge_indices])

    elif object_type == "rhombic triacontahedron":
        edge_indices = [
            (0, 8), (0, 12), (0, 16), (1, 8), (1, 13), (1, 17),
            (2, 9), (2, 12), (2, 18), (3, 9), (3, 13), (3, 19),
            (4, 10), (4, 14), (4, 16), (5, 10), (5, 15), (5, 17),
            (6, 11), (6, 14), (6, 18), (7, 11), (7, 15), (7, 19),
            (8, 9), (10, 11), (12, 14), (13, 15), (16, 17), (18, 19),
            (0, 4), (1, 5), (2, 6), (3, 7), (4, 8), (5, 9),
            (6, 10), (7, 11), (12, 16), (13, 17), (14, 18), (15, 19)
        ]
        edges = np.array([[vertices[i], vertices[j]] for i, j in edge_indices])
    

    drawObject(edges)

# draw each edge

def drawObject(edges):
    object.clear()  # clear the previous drawing

    for edge in edges:
        x1, y1 = edge[0][:2]
        x2, y2 = edge[1][:2]
        object.penup()
        object.goto(x1, y1)
        object.pendown()
        object.goto(x2, y2)

    screen.update()  # update the screen with the new drawing


def createObject():
    global vertices, object_type
    if object_type=="cube":
        vertices = np.array([
            [-1, -1, -1],
            [ 1, -1, -1],
            [ 1,  1, -1],
            [-1,  1, -1],
            [-1, -1,  1],
            [ 1, -1,  1],
            [ 1,  1,  1],
            [-1,  1,  1]
        ])

    if object_type=="pyramid":
        a, h = 2, 3

        # Pyramid vertices (4 base corners + 1 apex)
        vertices = np.array([[-a, -a, 0],  # Base vertex 1
        [-a,  a, 0],  # Base vertex 2
        [ a, -a, 0],  # Base vertex 3
        [ a,  a, 0],  # Base vertex 4
        [ 0,  0, h]]) # Apex
        
    if object_type=="cuboid":
        # Dimensions of the cuboid (half-lengths along each axis)
        a, b, c = 2, 1, 3

        # Cuboid vertices centered at origin
        vertices = np.array([[-a, -b, -c],
            [-a, -b,  c],
            [-a,  b, -c],
            [-a,  b,  c],
            [ a, -b, -c],
            [ a, -b,  c],
            [ a,  b, -c],
            [ a,  b,  c]])
    
    elif object_type == "dodecahedron":
        # Golden ratio
        phi = (1 + np.sqrt(5)) / 2
        
        vertices = np.array([
            [ 1,  1,  1], [-1,  1,  1], [ 1, -1,  1], [-1, -1,  1],
            [ 1,  1, -1], [-1,  1, -1], [ 1, -1, -1], [-1, -1, -1],
            [0,  1/phi,  phi], [0, -1/phi,  phi], [0,  1/phi, -phi], [0, -1/phi, -phi],
            [ phi, 0,  1/phi], [-phi, 0,  1/phi], [ phi, 0, -1/phi], [-phi, 0, -1/phi],
            [ 1/phi,  phi, 0], [-1/phi,  phi, 0], [ 1/phi, -phi, 0], [-1/phi, -phi, 0]
        ])
    
    elif object_type == "rhombic triacontahedron":
        # Golden ratio
        phi = (1 + np.sqrt(5)) / 2

        # Rhombic triacontahedron vertices
        vertices = np.array([
            [1, 1, 1], [-1, 1, 1], [1, -1, 1], [-1, -1, 1],
            [1, 1, -1], [-1, 1, -1], [1, -1, -1], [-1, -1, -1],
            [0, phi, 1/phi], [0, -phi, 1/phi], [0, phi, -1/phi], [0, -phi, -1/phi],
            [1/phi, 0, phi], [-1/phi, 0, phi], [1/phi, 0, -phi], [-1/phi, 0, -phi],
            [phi, 1/phi, 0], [-phi, 1/phi, 0], [phi, -1/phi, 0], [-phi, -1/phi, 0]
        ])

    

# object initialisation
object_type=input("What would you like to create? A cube/pyramid/cuboid: ")
scale=int(input("Enter the scale (1-100): "))
print("-----object initialised-----")
print("To view your object open up the new turtle window that has just appeared")
print("it can be controlled by using WASD to rotate around centre, arrow keys to move it, and =/- to increase/decrease scale")

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")

# Create a turtle to draw the object

object = turtle.Turtle()
object.speed(0) 
screen.tracer(0)
object.hideturtle()

# Create corresponding object

createObject()

# Scale object 
vertices = vertices * scale

object.color("white")   # Set the color of the trail to blue
object.pensize(3)      # Set the thickness of the trail


generateEdges() # generate edges and draw object




screen.listen()
# rotate
screen.onkeypress(lambda: transform_object(True,False,False,0.1,"rotate"), "s") 
screen.onkeyrelease(lambda: transform_object(True,False,False,0.1,"rotate"), "s")
screen.onkeypress(lambda: transform_object(True,False,False,-0.1,"rotate"), "w")  
screen.onkeyrelease(lambda: transform_object(True,False,False,-0.1,"rotate"), "w")  
screen.onkeypress(lambda: transform_object(False,True,False,0.1,"rotate"), "d")  
screen.onkeyrelease(lambda: transform_object(False,True,False,0.1,"rotate"), "d")  
screen.onkeypress(lambda: transform_object(False,True,False,-0.1,"rotate"), "a")  
screen.onkeyrelease(lambda: transform_object(False,True,False,-0.1,"rotate"), "a")  
screen.onkeypress(lambda: transform_object(False,False,True,0.1,"rotate"), "v")  
screen.onkeyrelease(lambda: transform_object(False,False,True,0.1,"rotate"), "v")  #

# translate
screen.onkeypress(lambda: transform_object(0,1,0,0,"translate"), "Up")  
screen.onkeyrelease(lambda: transform_object(0,1,0,0,"translate"), "Up")
screen.onkeypress(lambda: transform_object(0,-1,0,0,"translate"), "Down")  
screen.onkeyrelease(lambda: transform_object(0,-1,0,0,"translate"), "Down")  
screen.onkeypress(lambda: transform_object(1,0,0,0,"translate"), "Right")  
screen.onkeyrelease(lambda: transform_object(1,0,0,0.1,"translate"), "Right")  
screen.onkeypress(lambda: transform_object(-1,0,0,-0.1,"translate"), "Left")  
screen.onkeyrelease(lambda: transform_object(-1,0,0,-0.1,"translate"), "Left")  
screen.onkeypress(lambda: transform_object(0,0,1,0.1,"translate"), "m")  
screen.onkeyrelease(lambda: transform_object(0,0,1,0.1,"translate"), "m")  

# dilate
screen.onkeypress(lambda: transform_object(1,0,0,0,"dilate"), "=")  
screen.onkeypress(lambda: transform_object(-1,0,0,0,"dilate"), "-")  

# Keep the window open and responsive
screen.mainloop()
