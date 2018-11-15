import spectral.io.envi as envi
from IndianPines import IndianPines_Input
import numpy as np
from spectral import imshow, get_rgb
from scipy import ndimage, stats
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from pandas_ml import ConfusionMatrix




def modal(x):
    return stats.mode(x, axis=None)[0][0]

def mode_filter(img):
    return ndimage.generic_filter(img, modal, size=3)



def accuracy(input, img, train_positions, test_positions):

    correct_pixels_train, correct_pixels_test = [], []

    for (i, j) in train_positions:
        y_ = img[i, j]
        label = input.complete_gt[i, j]
        if label == y_:
            correct_pixels_train.append(1)
        else:
            correct_pixels_train.append(0)

    for (i, j) in test_positions:
        y_ = img[i, j]
        label = input.complete_gt[i, j]
        if label == y_:
            correct_pixels_test.append(1)
        else:
            correct_pixels_test.append(0)

    train_acc = np.asarray(correct_pixels_train).mean() * 100
    test_acc = np.asarray(correct_pixels_test).mean() * 100
    return train_acc, test_acc


def output_image(input, output):
    return get_rgb(output, color_scale=input.color_scale)


def clean_image(input, img):
    clean = np.zeros(shape=(input.height, input.width))

    for i in range(input.height):
        for j in range(input.width):

            label = img[i, j]

            if input.complete_gt[i, j] != 0:
                clean[i, j] = label


    return clean


def get_conf_matrix(input, img, test_positions):

    test_labels, test_predictions = [], []

    for (i, j) in test_positions:
        y_ = img[i, j]
        label = input.complete_gt[i, j]

        test_labels.append(label)
        test_predictions.append(y_)

    conf_matrix = ConfusionMatrix(test_labels, test_predictions)

    return conf_matrix


def apply_modal_filter(input, img, train_positions, test_positions):

    filt_img = img

    print("----------\nBefore filter")
    train_acc, test_acc = accuracy(input, filt_img, train_positions, test_positions)
    print("Training accuracy: %.2f" % train_acc)
    print("Test accuracy: %.2f" % test_acc)

    for n in range(5):
        print("---------------")
        print("Iteration " + str(n))
        filt_img = mode_filter(filt_img)

        train_acc, test_acc = accuracy(input, filt_img, train_positions, test_positions)
        print("Training accuracy: %.2f" %train_acc)
        print("Test accuracy: %.2f" %test_acc)

    # clean_img = clean_image(input, filt_img)
    clean_img = filt_img
    return clean_img, test_acc

#
#
# labelPatches = [patches.Patch(color=input.color_scale.colorTics[x+1]/255., label=input.class_names[x]) for x in range(input.num_classes) ]
#
#
# train_acc, test_acc = accuracy(input,img)
# view = output_image(input, img)
# # imshow(view)
# clean_img = clean_image(input, img)
# view = output_image(input, clean_img)
# # imshow(view)
#
#
#
#
# print("Training accuracy: %.2f" %train_acc)
# print("Test accuracy: %.2f" %test_acc)
#
# print("---------------")
# print("Modal filter")
# filt_img = img.load()
#
# for n in range(20):
#     print("---------------")
#     print("Iteration " + str(n))
#     filt_img = mode_filter(filt_img)
#
#     train_acc, test_acc = accuracy(input, filt_img)
#     print("Training accuracy: %.2f" %train_acc)
#     print("Test accuracy: %.2f" %test_acc)
#
# view = output_image(input, filt_img)
# fig = plt.figure(1)
# lgd = plt.legend(handles=labelPatches, ncol=1, fontsize='small', loc=2, bbox_to_anchor=(1, 1))
# imshow(view, fignum=1)
# fig.savefig("IndianPines/filt_lgd", bbox_extra_artists=(lgd,), bbox_inches='tight')
#
#
#
# clean_img = clean_image(input, filt_img)
# view = output_image(input, clean_img)
# fig = plt.figure(2)
# lgd = plt.legend(handles=labelPatches, ncol=1, fontsize='small', loc=2, bbox_to_anchor=(1, 1))
# imshow(view, fignum=2)
# fig.savefig("IndianPines/filt_clean_lgd", bbox_extra_artists=(lgd,), bbox_inches='tight')
# #
# envi.save_image("IndianPines/ip_filtro3_10it_96.hdr", filt_img, dtype='uint8', force=True, interleave='BSQ', ext='raw')
# #
