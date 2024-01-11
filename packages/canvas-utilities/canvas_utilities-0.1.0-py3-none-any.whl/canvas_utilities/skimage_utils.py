import matplotlib.pyplot as plt
from skimage import feature, filters

from .image_utils import load_image_data_array


@load_image_data_array
def detech_edge(data):
    edges = feature.canny(data, sigma=3)
    edge_sobel = filters.sobel(data)

    # display results
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                        sharex=True, sharey=True)

    ax1.imshow(data, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('mask image', fontsize=20)

    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Canny filter', fontsize=20)

    ax3.imshow(edge_sobel, cmap=plt.cm.gray)
    ax3.axis('off')
    ax3.set_title('sobel filter', fontsize=20)

    fig.tight_layout()
    plt.show()
