from PIL import Image
 
def colour_to_bw(img_path, grayscale=True, ow=False):
    #read the image from path
    image = Image.open('C:/Users/abc/Desktop/penguins.jpg')

    if grayscale:
        #Convert it into the grayscale image
        img = image.convert('L')

    else:
        #Converting the same image to black and white mode
        img = image.convert('1')

    if ow:
        # overwrite
        img.save(img_path)