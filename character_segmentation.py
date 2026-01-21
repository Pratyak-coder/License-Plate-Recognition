import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import filtering_unesseccery_blobs

# on the image I'm using, the headlamps were categorized as a license plate
# because their shapes were similar

def validate_plate(candidates):
        """
        validates the candidate plate objects by using the idea
        of vertical projection to calculate the sum of pixels across
        each column and then find the average.

        This method still needs improvement

        Parameters:
        ------------
        candidate: 3D Array containing 2D arrays of objects that looks
        like license plate

        Returns:
        --------
        a 2D array of the likely license plate region

        """
        if not candidates:
            return None

        for each_candidate in candidates:
            height, width = each_candidate.shape
            #each_candidate = inverted_threshold(each_candidate)
            license_plate = []
            highest_average = 0
            total_white_pixels = 0
            for column in range(width):
                total_white_pixels += sum(each_candidate[:, column])
            
            average = float(total_white_pixels) / width
            if average >= highest_average:
                license_plate = each_candidate

        return license_plate

license_plate = validate_plate(filtering_unesseccery_blobs.plate_like_objects)

# The invert was done so as to convert the black pixel to white pixel and vice versa
license_plate = np.invert(license_plate)

labelled_plate = measure.label(license_plate)

fig, ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")
# the next two lines is based on the assumptions that the width of
# a license plate should be between 5% and 15% of the license plate,
# and height should be between 35% and 60%
# this will eliminate some
character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.02*license_plate.shape[1], 0.15*license_plate.shape[1])
min_height, max_height, min_width, max_width = character_dimensions

characters = []
counter=0
column_list = []
for regions in regionprops(labelled_plate):
    y0, x0, y1, x1 = regions.bbox
    region_height = y1 - y0
    region_width = x1 - x0

    if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
        roi = license_plate[y0:y1, x0:x1]

        # draw a red bordered rectangle over the character.
        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rect_border)

        # resize the characters to 20X20 and then append each character into the characters list
        resized_char = resize(roi, (20, 20))
        characters.append(resized_char)

        # this is just to keep track of the arrangement of the characters
        column_list.append(x0)

plt.show()