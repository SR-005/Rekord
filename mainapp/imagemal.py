from PIL import Image,ImageDraw, ImageFilter

def imagemanipulation(image,prestige):
    img=Image.open(image).convert("RGBA")                   #load the image
    nftsize=1024
    pixelsize=9
    maxcolors=64
    glow_radius=5

    width,height=img.size                           #get the current dimentions
    mindimention=min(width,height)            #to get the minimum w and h without loosing quality and aspect ratio

    #aspects for cropping as a square
    left=(width-mindimention)//2
    right=left+mindimention

    top=(height-mindimention)//2
    bottom=top+mindimention

    croppedimage=img.crop((left,top,right,bottom))      #cropping the image
    nftimage=croppedimage.resize((nftsize,nftsize),Image.LANCZOS)   #resizing the cropped img to fit as nft

    #border seciton
    draw=ImageDraw.Draw(nftimage)
    if prestige=="standard":
        color="#46D12D"
        thickness=14
    elif prestige=="signature":
        color="#F1C40F"
        thickness=18
    elif prestige=="flagship":
        color="#8E44AD"
        thickness=22

    #glow section
    glow_layer = Image.new("RGBA", (nftsize, nftsize), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    for i in range(thickness):
        glow_draw.rectangle(
            [i, i, nftsize - i - 1, nftsize - i - 1],
            outline=color
        )

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow_radius))
    nftimage = Image.alpha_composite(nftimage, glow_layer)

    for i in range(thickness):
        draw.rectangle([i, i, nftsize-i-1, nftsize-i-1], outline=color)


    #pixeled image section
    pixelednft=nftimage.resize((nftsize//pixelsize, nftsize//pixelsize), resample=Image.BILINEAR)
    colorednft=pixelednft.quantize(colors=maxcolors)
    finalnft=colorednft.resize((nftsize,nftsize),resample=Image.NEAREST)


    finalnft.save("nftimage.png")
    return nftimage

def leveleditor(image):
    img=Image.open(str(image))
    return 0


if __name__ == "__main__":
    imagemanipulation("testimage.png")
    '''leveleditor("nftimage.png")'''