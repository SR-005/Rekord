from PIL import Image,ImageDraw

def imagemanipulation(image):
    img=Image.open(image)                   #load the image
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

    draw=ImageDraw.Draw(nftimage)

    prestige="hi"
    if prestige=="Standard":
        color="#887A66"
        thickness=8
    elif prestige=="Elite":
        color="#F1C40F"
        thickness=12
    else:
        color="#8E44AD"
        thickness=14

    for i in range(thickness):
        draw.rectangle([i, i, nftsize-i-1, nftsize-i-1], outline=color)

    nftimage.save("testimg.png")
    return nftimage

def leveleditor(image):
    img=Image.open(str(image))
    return 0


if __name__ == "__main__":
    imagemanipulation("nftimage.png")
    '''leveleditor("nftimage.png")'''