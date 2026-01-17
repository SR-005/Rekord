from PIL import Image,ImageDraw, ImageFilter, ImageFont

def imagemanipulation(image):
    img=Image.open(image).convert("RGBA")                   #load the image
    nftsize=1024
    prestige="flagship"
    loyality="short"

    width,height=img.size                           #get the current dimentions
    mindimention=min(width,height)            #to get the minimum w and h without loosing quality and aspect ratio

    #aspects for cropping as a square
    left=(width-mindimention)//2
    right=left+mindimention

    top=(height-mindimention)//2
    bottom=top+mindimention

    croppedimage=img.crop((left,top,right,bottom))      #cropping the image
    nftimage=croppedimage.resize((nftsize,nftsize),Image.LANCZOS)   #resizing the cropped img to fit as nft

    nftimage.save("nftimage.png")
    return nftimage

def loyality(image,prestige,loyality):
    nftimage=Image.open(str(image))
    nftsize=1024

    if loyality=="long":                                      #pixeled image section
        thickness=3
        pixelsize=5
        maxcolors=64

        pixelednft=nftimage.resize((nftsize//pixelsize, nftsize//pixelsize), resample=Image.BILINEAR)
        colorednft=pixelednft.quantize(colors=maxcolors)
        finalnft=colorednft.resize((nftsize,nftsize),resample=Image.NEAREST)

    elif loyality in ["short","medium"]:  # colored dot image section
        thickness = 0
        dotspacing = 7
        maxdotradius = 5

        # Grayscale for brightness
        gray = nftimage.convert("L")
        gray_pixels = gray.load()

        # White canvas
        dotted = Image.new("RGBA", (nftsize, nftsize), "white")
        dot_draw = ImageDraw.Draw(dotted)

        for y in range(0, nftsize, dotspacing):
            for x in range(0, nftsize, dotspacing):
                brightness = gray_pixels[x, y]  # 0–255

                # Darker pixel → bigger dot
                radius = int((255 - brightness) / 255 * maxdotradius)

                if radius > 0:
                    dot_draw.ellipse(
                        (
                            x - radius,
                            y - radius,
                            x + radius,
                            y + radius
                        ),
                        fill="black"
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
    return 0

def imagetest(image,prestige):

    # Open image
    img = Image.open(image).convert("RGB")
    TARGET_SIZE = 1024
    
    if prestige=="standard":
        bordercolor=(40,38,40)          #border color: grey-black
        textcolor = (255, 255, 255)     #text color: white
    elif prestige=="signature": 
        bordercolor=(252, 197, 33)      #border color: yellow-gold
        textcolor = (0, 0, 0)           #text color: black
    elif prestige=="flagship":
        bordercolor=(143,56,197)        #border color: purple
        textcolor = (255, 255, 255)     #text color: white
    else:
        print("Event Prestige Not Valid!!")

    # Borders
    border_top = 40
    border_left = 20
    border_right = 20
    border_bottom = 160

    # Image area
    target_w = TARGET_SIZE - (border_left + border_right)
    target_h = TARGET_SIZE - (border_top + border_bottom)

    # --- Crop to fit ---
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    img = img.resize((target_w, target_h), Image.LANCZOS)

    # --- Canvas (border color here) ---
    canvas = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), bordercolor)
    canvas.paste(img, (border_left, border_top))




    # --- Draw text ---
    draw = ImageDraw.Draw(canvas)

    # Load Roca Two font
    font = ImageFont.truetype("Roca_Two_Bold.ttf", 104)

    text = "TINK-HER-HACK"
    
    # Measure text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Position text - Event Name
    mainx = (TARGET_SIZE - text_w) // 2
    mainy = TARGET_SIZE - border_bottom + (border_bottom - text_h) // 2
    mainy-=36
    draw.text((mainx, mainy), text, fill=textcolor, font=font)


    font = ImageFont.truetype("Roca_Two_Bold.ttf", 58)
    text = "by tinkerhub"
    # Measure text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Position text - Event Name
    mainx = (TARGET_SIZE - text_w) //1.03
    mainy = TARGET_SIZE - border_bottom + (border_bottom - text_h) // 2
    mainy+=40
    draw.text((mainx, mainy), text, fill=textcolor, font=font)

    # Save
    canvas.save("nftimage.png")




if __name__ == "__main__":
    '''imagemanipulation("testimage3.png")'''
    '''loyality("testimage3.png","flagship","short")'''
    imagetest("testimage.png","flagship")
#standard
#signature
#flagship