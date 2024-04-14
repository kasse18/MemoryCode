# Импорт библиотек
import numpy as np
import matplotlib.pyplot as plt
import cv2


def back_to_color(image):
    # Путь к нашим файлам caffemodel, prototxt и numpy
    prototxt = "./colorization_models/colorization_deploy_v2.prototxt"
    caffe_model = "./colorization_models/colorization_release_v2.caffemodel"
    pts_npy = "./colorization_models/pts_in_hull.npy"

    test_image = "./input_images/" + image

    # Загрузка нашей модели
    net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)
    pts = np.load(pts_npy)

    layer1 = net.getLayerId("class8_ab")
    print(f'Слой "class8_ab", id ={layer1}')
    layer2 = net.getLayerId("conv8_313_rh")
    print(f'Слой "conv8_313_rh", id ={layer2}')
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(layer1).blobs = [pts.astype("float32")]
    net.getLayer(layer2).blobs = [np.full([1, 313], 2.606, dtype="float32")]


    test_image = cv2.imread(test_image)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    test_image = cv2.cvtColor(test_image, cv2.COLOR_GRAY2RGB)

    normalized = test_image.astype("float32") / 255.0

    lab_image = cv2.cvtColor(normalized, cv2.COLOR_RGB2LAB)

    # Изменение размера изображения
    resized = cv2.resize(lab_image, (224, 224))

    # Извлечение значения L для изображения LAB
    L = cv2.split(resized)[0]
    L -= 50  # OR we can write L = L - 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (test_image.shape[1], test_image.shape[0]))

    L = cv2.split(lab_image)[0]
    LAB_colored = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    RGB_colored = cv2.cvtColor(LAB_colored, cv2.COLOR_LAB2RGB)

    RGB_colored = np.clip(RGB_colored, 0, 1)
    RGB_colored = (255 * RGB_colored).astype("uint8")

    RGB_BGR = cv2.cvtColor(RGB_colored, cv2.COLOR_RGB2BGR)

    # Сохранение изображения в нужном месте
    cv2.imwrite("./output_images/" + image, RGB_BGR)


if __name__ == '__main__':
    back_to_color("1652.jpg")