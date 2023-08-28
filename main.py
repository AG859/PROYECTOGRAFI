import shaders
from gl import Renderer, V2, color

width = 2100
height = 1800

rend = Renderer(width,height)


rend.glBackgroundTexture("bosque.bmp")
rend.glClearBackground()

rend.vertexShader = shaders.vertexShader

rend.camera.update_view_projection(look_at_point=[rend.camera.position[0], rend.camera.position[1] - 100, rend.camera.position[2]], up_direction=[0, 1, 0])

rend.glLoadModel(filename="model1.obj", textureName="model1.bmp", 
                translate=(width/2 - 400, height/2 - 350, 0), 
                rotate=(180,0,270), 
                scale=(10,10,10), fragmentShader=shaders.fragmentShader4)




rend.fragmentShader = shaders.fragmentShader2
rend.glLoadModel(filename="model2.obj", textureName="model2.bmp", 
                        translate=(width/2 + 100, height/2 - 250, 0), 
                rotate=(180,0,180), 
                scale=(10,10,10), fragmentShader=shaders.fragmentShader2)


rend.glLoadModel(filename="model3.obj", textureName="model3.bmp", 
               translate=(width/2 + 500, height/2 - 250, 0), 
              rotate=(180,0,180), 
               scale=(10,10,10) ,fragmentShader=shaders.fragmentShader1) 

# # rend.glLoadModel(filename="model4.obj", textureName="model4.bmp", 
# #                translate=(width/2 + 700, height/2 - 250, 0), 
# #               rotate=(180,0,270), 
# #                scale=(10,10,10))  # Ajuste de escala si es necesario


rend.fragmentShader = shaders.fragmentShader2
rend.glLoadModel(filename="model5.obj", textureName="model5.bmp", 
               translate=(width/2 + 700, height/2 - 650, 0), 
              rotate=(180,0,270), 
               scale=(5,5,5), fragmentShader=shaders.fragmentShader3) 

rend.glRender()
rend.glFinish("output2.bmp")
