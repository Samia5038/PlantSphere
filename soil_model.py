from pathlib import Path

import joblib
import numpy as np
from PIL import Image, ImageStat
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = Path(__file__).resolve().parent
TRAIN_DIR = BASE_DIR / "Dataset" / "Train"
TEST_DIR = BASE_DIR / "Dataset" / "test"
MODEL_PATH = BASE_DIR / "instance" / "soil_model.joblib"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CLASS_NAMES = {
    "alluvial soil": "alluvial",
    "black soil": "black",
    "clay soil": "clay",
    "red soil": "red",
}
RESIZE = (16, 16)
HISTOGRAM_BINS = 16


def extract_image_features(image):
    rgb_image = image.convert("RGB")
    sample = rgb_image.resize(RESIZE, Image.Resampling.BILINEAR)
    rgb = np.asarray(sample, dtype=np.float32) / 255.0
    hsv = np.asarray(sample.convert("HSV"), dtype=np.float32) / 255.0
    gray = np.asarray(sample.convert("L"), dtype=np.float32) / 255.0

    features = [rgb.reshape(-1)]
    for color_image in (rgb, hsv):
        for channel in range(3):
            histogram, _ = np.histogram(
                color_image[:, :, channel], bins=HISTOGRAM_BINS, range=(0.0, 1.0)
            )
            features.append(histogram.astype(np.float32) / color_image.shape[0] / color_image.shape[1])

    features.append(np.histogram(gray, bins=HISTOGRAM_BINS, range=(0.0, 1.0))[0].astype(np.float32) / gray.size)

    for row in range(4):
        for column in range(4):
            tile = rgb[row * 4:(row + 1) * 4, column * 4:(column + 1) * 4]
            features.extend((tile.mean(axis=(0, 1)), tile.std(axis=(0, 1))))

    return np.concatenate(features)


def _read_split(folder):
    if not folder.is_dir():
        raise FileNotFoundError("Soil image folder was not found: {}".format(folder))

    image_features = []
    labels = []
    counts = {}
    skipped = 0
    for class_folder in sorted(path for path in folder.iterdir() if path.is_dir()):
        class_name = CLASS_NAMES.get(class_folder.name.strip().casefold())
        if class_name is None:
            continue
        counts[class_name] = 0
        for image_path in sorted(class_folder.rglob("*")):
            if not image_path.is_file() or image_path.suffix.casefold() not in IMAGE_EXTENSIONS:
                continue
            try:
                with Image.open(image_path) as image:
                    image_features.append(extract_image_features(image))
                labels.append(class_name)
                counts[class_name] += 1
            except (OSError, ValueError) as error:
                skipped += 1
                print("Skipping unreadable image {}: {}".format(image_path, error))

    if not labels:
        raise ValueError("No readable soil images found under {}".format(folder))
    if skipped:
        print("Skipped {} unreadable image(s) in {}".format(skipped, folder.name))
    return np.vstack(image_features), np.asarray(labels), counts


def train_soil_model(model_path=MODEL_PATH):
    train_features, train_labels, train_counts = _read_split(TRAIN_DIR)
    test_features, test_labels, test_counts = _read_split(TEST_DIR)
    expected_classes = set(train_counts)
    if expected_classes != set(test_counts):
        raise ValueError("Train and test folders must contain the same soil class folders.")

    classifier = ExtraTreesClassifier(
        n_estimators=180,
        max_features="sqrt",
        max_depth=24,
        min_samples_leaf=2,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42,
    )
    classifier.fit(train_features, train_labels)

    predictions = classifier.predict(test_features)
    accuracy = accuracy_score(test_labels, predictions)
    report = classification_report(
        test_labels,
        predictions,
        labels=sorted(expected_classes),
        output_dict=True,
        zero_division=0,
    )
    payload = {
        "model": classifier,
        "classes": list(classifier.classes_),
        "accuracy": float(accuracy),
        "report": report,
        "train_counts": train_counts,
        "test_counts": test_counts,
    }

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, model_path)
    print("Training images:", train_counts)
    print("Test images:", test_counts)
    print("Test accuracy: {:.1%}".format(accuracy))
    print(classification_report(test_labels, predictions, labels=sorted(expected_classes), zero_division=0))
    print("Saved soil model to {}".format(model_path))
    return payload


def load_soil_model(model_path=MODEL_PATH):
    model_path = Path(model_path)
    if model_path.exists():
        try:
            return joblib.load(model_path)
        except (OSError, EOFError, ValueError, AttributeError):
            print("Saved soil model is invalid; training a fresh model.")
    return train_soil_model(model_path)


def classify_soil_image(image, payload):
    features = extract_image_features(image).reshape(1, -1)
    model = payload["model"]
    probabilities = model.predict_proba(features)[0]
    index = int(np.argmax(probabilities))
    return {
        "soil_type": str(model.classes_[index]),
        "confidence": float(probabilities[index]),
        "test_accuracy": float(payload["accuracy"]),
    }


if __name__ == "__main__":
    train_soil_model()