from PIL import Image,ImageDraw, ImageFilter

def imagemanipulation(image,prestige,loyality):
    img=Image.open(image).convert("RGBA")                   #load the image
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

    if loyality=="long":                                      #pixeled image section
        thickness=3
        pixelsize=5
        maxcolors=64

        pixelednft=nftimage.resize((nftsize//pixelsize, nftsize//pixelsize), resample=Image.BILINEAR)
        colorednft=pixelednft.quantize(colors=maxcolors)
        finalnft=colorednft.resize((nftsize,nftsize),resample=Image.NEAREST)

    elif loyality in ["short","medium"]:  # colored dot image section
        thickness=0
        dotspacing = 8
        maxdotradius = 5

        # Grayscale for brightness
        gray = nftimage.convert("L")
        gray_pixels = gray.load()

        # RGB for color
        color_pixels = nftimage.convert("RGB").load()

        # White canvas
        dotted = Image.new("RGBA", (nftsize, nftsize), "white")
        dot_draw = ImageDraw.Draw(dotted)

        for y in range(0, nftsize, dotspacing):
            for x in range(0, nftsize, dotspacing):
                brightness = gray_pixels[x, y]  # ✅ int 0–255

                radius = int((255 - brightness) / 255 * maxdotradius)

                if radius > 0:
                    r, g, b = color_pixels[x, y]  # ✅ tuple
                    dot_draw.ellipse(
                        (
                            x - radius,
                            y - radius,
                            x + radius,
                            y + radius
                        ),
                        fill=(r, g, b)
                    )

        finalnft = dotted

    #border seciton
    draw=ImageDraw.Draw(finalnft)
    if prestige=="standard":
        color="#46D12D"
        thickness=thickness+8
    elif prestige=="signature":
        color="#F1C40F"
        thickness=thickness+10
    elif prestige=="flagship":
        color="#8E44AD"
        thickness=thickness+12

    #glow section
    glow_radius=3
    glow_layer = Image.new("RGBA", (nftsize, nftsize), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    for i in range(thickness):
        glow_draw.rectangle(
            [i, i, nftsize - i - 1, nftsize - i - 1],
            outline=color
        )

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow_radius))
    finalnft = finalnft.convert("RGBA")
    finalnft = Image.alpha_composite(finalnft, glow_layer)

    for i in range(thickness):
        draw.rectangle([i, i, nftsize-i-1, nftsize-i-1], outline=color)




    finalnft.save("nftimage.png")
    return nftimage

def leveleditor(image):
    img=Image.open(str(image))
    return 0


if __name__ == "__main__":
    imagemanipulation("testimage.png","flagship","long")
    '''leveleditor("nftimage.png")'''