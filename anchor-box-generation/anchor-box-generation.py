import math

def generate_anchors(feature_size, image_size, scales, aspect_ratios):
    """
    Generate anchor boxes for object detection.
    """
    # Write code here
    stride = image_size / feature_size

    anchors = []

    for i in range(feature_size):
        for j in range(feature_size):
            c_x = (j+0.5) * stride
            c_y  = (i+0.5) * stride

            for s in scales:
                for r in aspect_ratios:
                    w = s * math.sqrt(r)
                    h = s / math.sqrt(r)

                    anchors.append([c_x - (w/2), c_y - (h/2), c_x + (w/2), c_y + (h/2)])

    return anchors
            