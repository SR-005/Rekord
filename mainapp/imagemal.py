from PIL import Image,ImageDraw, ImageFilter, ImageFont

def prestige(img,prestige):
    img=img.convert("RGB")
    imagesize=1024
    
    if prestige=="standard":
        bordercolor=(40,38,40)          #border color: grey-black
        textcolor = (255, 255, 255)     #text color: white
        organizationnamecolor=(255, 255, 255)   #org name color: white
    elif prestige=="signature": 
        bordercolor=(252, 197, 33)      #border color: yellow-gold
        textcolor = (0, 0, 0)           #text color: black
        organizationnamecolor=(143,56,197)      #org name color: purple
    elif prestige=="flagship":
        bordercolor=(143,56,197)        #border color: purple
        textcolor = (255, 255, 255)     #text color: white
        organizationnamecolor=(0,0,0)   #org name color: black
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
    organizationname = "by tinkerhub"
    # Measure text size
    bbox = draw.textbbox((0, 0), organizationname, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Position text - Event Name
    mainx = (imagesize - text_w) //1.03
    mainy =imagesize - borderbottom+ (borderbottom- text_h) // 2
    mainy+=40
    draw.text((mainx, mainy), organizationname, fill=organizationnamecolor, font=font)

    return canvas
    #canvas.save("prestigeimage.png")

def imagemanipulation(image,prestigelevel):
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

    #nftimage.save("nftimage.png")
    image=prestige(nftimage,prestigelevel)
    return image

def loyality(image,loyality):

    #Open Image, Draw and Canvas
    img=Image.open(image).convert("RGB")
    imagesize=1024

    # Borders
    bordertop=40
    borderleft=20
    borderright=20
    borderbottom=160    

    # Image area
    cropped_imagewidth=imagesize-(borderleft+ borderright)
    cropped_imageheight=imagesize-(bordertop+ borderbottom)

    canvas = Image.new("RGB", (imagesize, imagesize), (0, 0, 0))
    canvas.paste(img)
    draw = ImageDraw.Draw(canvas)

    #loyality levels
    if loyality=="short":
        gray_img = img.convert("L").convert("RGB")  
        canvas.paste(gray_img)

    elif loyality=="medium":
        pass

    elif loyality=="long":

        headercolor1=(143,56,197)        #header color: purple
        headercolor2=(0,0,0)        #header color: purple
        

        #draw bounding box for the image inside border
        x1=borderleft
        y1=bordertop
        x2=borderleft+ cropped_imagewidth
        y2=bordertop+ cropped_imageheight

        image_height = y2 - y1
        headertext1 = "REKORD FLAGSHIP NFT"
        font = ImageFont.truetype("Roca_Two_Bold.ttf", 22)

        # Measure text
        bbox = draw.textbbox((0, 0), headertext1, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # X: center within image bbox
        offsetx=-350
        text_x = x1 + (x2 - x1 - text_w) // 2 + offsetx

        # Y: inside image, near top
        top_offset_ratio = 0.01 
        text_y = y1 + int(image_height * top_offset_ratio)

        draw.text((text_x, text_y), headertext1, fill=headercolor1, font=font)

        headertext2 = "0xDFDa8340978B38d93114FAE615144e895A75ebb2"
        font = ImageFont.truetype("Roca_Two_Bold.ttf", 16)

        # Measure text
        bbox = draw.textbbox((0, 0), headertext2, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # X: center within image bbox
        offsetx=290
        text_x = x1 + (x2 - x1 - text_w) // 2 + offsetx

        # Y: inside image, near top
        top_offset_ratio = 0.01 
        text_y = y1 + int(image_height * top_offset_ratio)

        draw.text((text_x, text_y), headertext2, fill=headercolor2, font=font)
    else:
        print("Loyality level is Invalid!!")

    # Save
    canvas.save("loyalityimage.png")
    canvas.save("loyalityimage.png")


if __name__ == "__main__":
    imagemanipulation(0,0)
    '''prestige("testimage.png","signature")
    loyality("prestigeimage.png","long")'''
#standard
#signature
#flagship

#short
#medium
#long