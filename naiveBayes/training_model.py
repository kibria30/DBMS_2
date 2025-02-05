import numpy as np
import cv2

# Count of Skin Colors
skin_rgb_cnt = np.empty(shape=(256, 256, 256))
skin_rgb_cnt.fill(0)

# Count of Non-Skin Colors
non_skin_rgb_cnt = np.empty(shape=(256, 256, 256))
non_skin_rgb_cnt.fill(0)

total_skin_color = 0
total_non_skin_color = 0
total_images = 555
indices = ["%04d" % x for x in range(1000)]


for index in range(total_images): 
    mask_image = cv2.imread("Mask/" + str(indices[index]) + ".bmp")
    actual_image = cv2.imread("ibtd/" + str(indices[index]) + ".jpg")
    height, width, channel = mask_image.shape

    for x in range(height):
        for y in range(width):
            mask_blue = mask_image[x, y, 0]
            mask_green = mask_image[x, y, 1]
            mask_red = mask_image[x, y, 2]

            blue = actual_image[x, y, 0]
            green = actual_image[x, y, 1]
            red = actual_image[x, y, 2]

            if mask_blue > 250 and mask_green > 250 and mask_red > 250:  # means it's NON-SKIN
                non_skin_rgb_cnt[red, green, blue] += 1
                total_non_skin_color += 1
            else:
                skin_rgb_cnt[red, green, blue] += 1
                total_skin_color += 1

    print("Image ", index, " - DONE!")


P_skin = total_skin_color / (total_skin_color + total_non_skin_color)      # P(S)
P_non_skin = total_non_skin_color / (total_skin_color + total_non_skin_color)  # P(NS)
    
with open('output.txt', 'w') as fp:
    for r in range(256):
        for g in range(256):
            for b in range(256):
                P_color_given_skin = skin_rgb_cnt[r, g, b] / total_skin_color        # P(C|S)
                P_color_given_non_skin = non_skin_rgb_cnt[r, g, b] / total_non_skin_color  # P(C|NS)
                
                P_color = (P_color_given_skin * P_skin + 
                            P_color_given_non_skin * P_non_skin)
                
                if P_color > 0:
                    P_skin_given_color = (P_color_given_skin * P_skin) / P_color
                else:
                    P_skin_given_color = 0.0
                
                # Write posterior probability to file
                fp.write(f"{P_skin_given_color}\n")

fp.close()
