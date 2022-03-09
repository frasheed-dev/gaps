import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook
import cv2

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


class Plot(object):

    def __init__(self, image, title="Initial problem"):
        aspect_ratio = image.shape[0] / float(image.shape[1])

        width = 8
        height = width * aspect_ratio
        fig = plt.figure(figsize=(width, height), frameon=False)

        # Let image fill the figure
        ax = plt.Axes(fig, [0., 0., 1., .9])
        ax.set_axis_off()
        fig.add_axes(ax)

        self._current_image = ax.imshow(image, aspect="auto", animated=True)
        self.show_fittest(image, title)

    def show_fittest(self, image, title, file_name="test.jpg"):
        plt.suptitle(title, fontsize=20)
        self._current_image.set_data(image)
        #plt.draw()
        cv2.imwrite(file_name, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        
        # Give pyplot 0.05s to draw image
        #plt.pause(0.05)
