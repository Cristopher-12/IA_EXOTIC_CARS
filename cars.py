import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import json

urls = ('/upload', 'Upload')

class Upload ():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html>
        <html><head><meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	    <title>IA EXOTIC CARS</title>
	    <!-- CSS only -->
	    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
     crossorigin="anonymous"></head><body><div class="container bg-light ">
     <center>
		        <div class="row justify-content-center mt-4 pt-4">
			            <div class="col-md-10 ">
            <a href="https://ibb.co/f0kKwRQ"><img src="https://imgbb.com/"><img src="https://i.ibb.co/HgtM8vX/AI.png" alt="AI" border="0"></a>
            <br>
            <br>
            <br>
             <label class="h1">IA EXOTIC CARS</label> <br>
             <br><br>
                 <form method="POST" enctype="multipart/form-data" action="">
                 <input type="file" name="myfile" />
                <br/><br/>
                <button  class="btn btn-secondary input type="submit"> Analizar </button> <br> <br> 
                  </form>
        </center>
        </body>
        </div></<div>
        </html>
</html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = 'static' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        
        #raise web.seeother('/upload')

# Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

# Load the model
        model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
        image = Image.open('/workspace/IA_EXOTIC_CARS/static/'+filename)

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
        #print(prediction) backup
# NAME OF RECOGNIZED OBJECT
        for i in prediction:
            if i [0] > 0.5:
                data= "NISSAN GTR"
                return data
            elif i [1] > 0.5:
                data= "FORD MUSTANG"
                return data
            elif i [2] > 0.5:
                data= "LAMBORGHINI HURACAN PERFOMANTE"
                return data
            
            else:
                auto="Auto no reconocido"
            return json.dumps(datos)

            
 datos = {
            titulo: [
            ]
        }

        car = {}
        car["resultado"] = resultado
        car["descripcion"] = descripcion
        car["status"] = status
        datos[titulo].append(car)
        return json.dumps(datos)


if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
    