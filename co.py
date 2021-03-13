import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np



urls = ('/upload', 'Upload')

class Upload ():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html>
        <html><head><meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>What stung me?</title>
	<!-- CSS only -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
     crossorigin="anonymous"></head><body><div class="container bg-light ">
     <center>
		<div class="row justify-content-center mt-4 pt-4">
			<div class="col-md-10 ">
            <a href="https://ibb.co/27Dn5xh"><img src="https://i.ibb.co/27Dn5xh/logo.png" alt="logo" border="0" ></a>
            <br>
            <br>
            <br>
             <label class="h1">What stung me?</label> <br>
             <br><br>
                 <form method="POST" enctype="multipart/form-data" action="">
                 <input type="file" name="myfile" />
                <br/><br/>
                <button  class="btn btn-secondary input type="submit"> Subir </button> <br> <br> 
                  </form>
        </center>
        </body>
        </div></<div>
        </html>
</html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = '/workspace/Picaduras/picaduras/static' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
     
        np.set_printoptions(suppress=True)
        # Disable scientific notation for clarity


            # Load the model
        model = tensorflow.keras.models.load_model('/workspace/Picaduras/picaduras/static/keras_model.h5')
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
        image = Image.open('/workspace/Picaduras/picaduras/static/'+filename)

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
        image_array = np.asarray(image)

# display the resized image
        image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

# run the inference
        prediction = model.predict(data)

        for i in prediction:
            if i[0] > 0.7:
                data= "Picadura de Araña\n Limpie el área con agua y jabón.Ayude a la persona a permanecer calmada para reducir la propagación del veneno; no aplique ningún torniquete. Aplique una compresa fría o una bolsa de hielo envuelta en un paño."
                return data
            elif i[1] > 0.7:
                data= "Picadura de Abeja \n Lavar la zona afectada con agua y jabón.Enfriar la picadura con hielo.Aplicar un antiséptico.Nunca se debe apretar la picadura de abeja o avispa para tratar de sacar el veneno,  ya que este puede extenderse \nSe puede paliar el dolor y las molestias con una crema para el picor y un antihistamínico"
                return data
            elif i[2] > 0.7:
                data="Picadura de Hormiga \n Si alguna vez crees que te ha picado una hormiga. El veneno de las picaduras de hormigas coloradas puede producir una ligera hinchazón en la zona de la picadura, y puede que el médico quiera echarle un vistazo para asegurarse de que no tienes una reacción alérgica."
                return data
            elif i[3] > 0.7:
                data="Picadura de Garrapata\n Utiliza pinzas pequeñas o de punta fina para agarrar la garrapata lo más cerca posible de la piel. Saca suavemente la garrapata con un movimiento ascendente lento y constante. No la tuerzas ni la aprietes. No agarres la garrapata con las manos desprotegidas.\n Los expertos no recomiendan usar vaselina, esmalte de uñas ni cerillas (fósforos) calientes para quitar garrapatas."
                return data
            elif i[4] > 0.7:
                data="Picadura de Mosquito \n Aplica loción, crema o pasta.Aplicar una loción de calamina o una crema de hidrocortisona de venta libre en la picadura puede ayudar a aliviar la picazón. O bien, prueba a untar la picadura con una pasta preparada con bicarbonato de sodio y agua. Vuelve a aplicarla varias veces al día hasta que los síntomas desaparezcan. \nAplica una compresa fría. Intenta calmar la picadura aplicando una compresa fría o un paño frío y húmedo durante unos minutos.Toma un antihistamínico oral. Para las reacciones más fuertes, prueba tomando un antihistamínico de venta libre (Benadryl, Chlor-Trimeton y otros)."
                return data
            elif i[5] > 0.7:
                data="Picadura de Pulga \n Si crees que te ha picado una pulga, lava la picadura con agua y jabón. Aplica loción de calamina para aliviar la picazón, o un adulto puede conseguirte en la farmacia una crema que alivie la picazón. Trata de no rascarte demasiado porque las picaduras podrían infectarse"
                return data
            elif i[6] > 0.7:
                data= "Picadura de Chinche \n Si crees que te ha picado una chinche, lava la picadura con agua y jabón y ponte loción de calamina para aliviar el picor. Un adulto te puede conseguir una crema para aliviar la picazón en una farmacia o droguería.\n Intenta rascarte la picadura lo menos posible porque se te podría infectar."
                return data
            else:
                picadura= "No se reconoce la Picadura"
            return picadura



if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()