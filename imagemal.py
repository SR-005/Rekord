from PIL import Image

def imagemanipulation(imgname):
    defaultinpath="media/icons/"
    inputpath=defaultinpath+imgname         #generating input path

    img=Image.open(inputpath)                   #load the image
    nftsize=1024

    width,height=img.size                           #get the current dimentions
    mindimention=min(width,height)            #to get the minimum w and h without loosing quality and aspect ratio

    #aspects for cropping as a square
    left=(width-mindimention)//2
    right=left+mindimention

    top=(height-mindimention)//2
    bottom=top+mindimention

    croppedimage=img.crop((left,top,right,bottom))      #cropping the image
    nftimage=croppedimage.resize((nftsize,nftsize),Image.LANCZOS)   #resizing the cropped img to fit as nft

    defaultoutpath="media/nft_badge/"
    outputpath=defaultoutpath+imgname           #generating output path
    nftimage.save(outputpath)
