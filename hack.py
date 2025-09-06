from PIL import Image 
 
def encode_message(image_path,message,output_path):
    img=Image.open ("C:/Users/Nikhi/Downloads/download.png")
    
    binary_message=''.join(format(ord(i),'08b')for i in message) + '1111111111111110'
    data=iter(img.getdata()) 
    
    new_pixels=[]
    msg_index=0
    
    for pixel in data:
        pixel=list(pixel)
        for i in range(3):
            if msg_index<len(binary_message):
                pixel[i]=pixel[i]& ~1 |int(binary_message[msg_index])
                msg_index +=1
        new_pixels.append(tuple(pixel))
    img.putdata(new_pixels)
    img.save(output_path)
    print("Message encoded and saved to",output_path)
    
def decode_message (image_path):
    img=Image.open(image_path)
    data = iter(img.getdata())
    
    binary_message=''
    for pixel in data:
        for i in range(3):
            binary_message += str(pixel[i]&1)
            if binary_message[-16:]=='1111111111111110':
                binary_message=binary_message[:-16]
                
                message=''.join(chr(int(binary_message[i:i+8],2))for i in range(0,len(binary_message),8))
                return message
    return "No hidden message found!"
        
encode_message("C:/Users/Nikhi/Downloads/download.png",'Hello, World!',"C:/Users/Nikhi/Downloads/encoded_image.png")

print("decoded message:", decode_message ("C:/Users/Nikhi/Downloads/encoded_image.png"))    
                