ef load_model() -> Any:
    # Load serialized black and white colorizer model and cluster
    # The L channel encodes lightness intensity only
    # The a channel encodes green-red.
    # And the b channel encodes blue-yellow
    print("Загрузка модели...")

    prototxt = "colorization_models/colorization_deploy_v2.prototxt"
    model = "colorization_models/colorization_release_v2.caffemodel"
    points = "colorization_models/pts_in_hull.npy"

    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    pts = np.load(points)

    # Add the cluster centers as 1x1 convolutions to the model:

    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    return net

def colorize_image(net: Any, image_in: str, image_out: str):
    # Load the input image, scale it and convert it to Lab:
    image = cv2.imread(image_in)
    height, width, channels = image.shape
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Extracting "L"
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)

    # Resize to network size
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Predicting "a" and "b"
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    # Creating a colorized Lab photo (L + a + b)
    L = cv2.split(lab)[0]
    ab = cv2.resize(ab, (width, height))
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    # Convert to RGB
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    cv2.imwrite(image_out, cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR))
    print("Изображение %s сохранено" % image_out)
