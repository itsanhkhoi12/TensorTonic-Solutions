def color_to_grayscale(image):
    """
    Convert an RGB image to grayscale using luminance weights.
    """
    # Write code here

    grayscale = []

    for i in image:
        print(i)
        pixels = []
        for j in i:
            pixels.append((j[0]*0.299)+(j[1]*0.587)+(j[2]*0.114))

        grayscale.append(pixels)
        
    return grayscale