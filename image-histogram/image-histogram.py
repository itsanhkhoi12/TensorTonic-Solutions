def image_histogram(image):
    """
    Compute the intensity histogram of a grayscale image.
    """
    # Write code here
    histogram = [0] * 256

    flatten_img = []
    
    for pixels in image:
        flatten_img.extend(pixels)

    for i in range(len(flatten_img)):
        histogram[flatten_img[i]]+=1

    return histogram
        