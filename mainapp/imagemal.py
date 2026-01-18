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



def imagetest(image,prestige,loyality):

    # Open image
    img=Image.open(image).convert("RGB")
    imagesize=1024
    
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
    bordertop=40
    borderleft=20
    borderright=20
    borderbottom=160

    # Image area
    cropped_imagewidth=imagesize-(borderleft+ borderright)
    cropped_imageheight=imagesize-(bordertop+ borderbottom)

    # --- Crop to fit ---
    original_imageratio=img.width/img.height
    cropped_imageratio=cropped_imagewidth/cropped_imageheight

    if original_imageratio>cropped_imageratio:
        new_width=int(img.height * cropped_imageratio)
        left=(img.width - new_width) // 2
        img=img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / cropped_imageratio)
        top=(img.height - new_height) // 2
        img=img.crop((0, top, img.width, top + new_height))

    img=img.resize((cropped_imagewidth, cropped_imageheight), Image.LANCZOS)

    # --- Canvas (border color here) ---
    canvas=Image.new("RGB", (imagesize,imagesize), bordercolor)
    canvas.paste(img, (borderleft, bordertop))




    # --- Draw text ---
    draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype("Roca_Two_Bold.ttf", 104)

    text="TINK-HER-HACK"
    
    # Measure text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Position text - Event Name
    mainx = (imagesize - text_w) // 2
    mainy =imagesize - borderbottom+ (borderbottom- text_h) // 2
    mainy-=36
    draw.text((mainx, mainy), text, fill=textcolor, font=font)


    font = ImageFont.truetype("Roca_Two_Bold.ttf", 58)
    text = "by tinkerhub"
    # Measure text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Position text - Event Name
    mainx = (imagesize - text_w) //1.03
    mainy =imagesize - borderbottom+ (borderbottom- text_h) // 2
    mainy+=40
    draw.text((mainx, mainy), text, fill=textcolor, font=font)

    #loyality levels
    if loyality=="short":
        gray_img = img.convert("L").convert("RGB")  
        canvas.paste(gray_img, (borderleft, bordertop))

    elif loyality=="medium":
        pass

    elif loyality=="long":
        #draw bounding box for the image inside border
        x1=borderleft
        y1=bordertop
        x2=borderleft+ cropped_imagewidth
        y2=bordertop+ cropped_imageheight

        image_height = y2 - y1
        label = "REKORD FLAGSHIP NFT"
        font = ImageFont.truetype("Roca_Two_Bold.ttf", 22)
        text_color = (0,0,0)

        # Measure text
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # X: center within image bbox
        offsetx=-350
        text_x = x1 + (x2 - x1 - text_w) // 2 + offsetx

        # Y: inside image, near top
        top_offset_ratio = 0.01 
        text_y = y1 + int(image_height * top_offset_ratio)

        draw.text((text_x, text_y), label, fill=text_color, font=font)


        label = "0xDFDa8340978B38d93114FAE615144e895A75ebb2"
        font = ImageFont.truetype("Roca_Two_Bold.ttf", 16)
        text_color = (0,0,0)

        # Measure text
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # X: center within image bbox
        offsetx=290
        text_x = x1 + (x2 - x1 - text_w) // 2 + offsetx

        # Y: inside image, near top
        top_offset_ratio = 0.01 
        text_y = y1 + int(image_height * top_offset_ratio)

        draw.text((text_x, text_y), label, fill=text_color, font=font)
    else:
        print("Loyality level is Invalid!!")

    # Save
    canvas.save("nftimage.png")




if __name__ == "__main__":
    '''imagemanipulation("testimage3.png")'''
    '''loyality("testimage3.png","flagship","short")'''
    imagetest("testimage.png","flagship","short")
#standard
#signature
#flagship

#short
#medium
#long