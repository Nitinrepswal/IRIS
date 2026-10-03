from core.vision import VisionEngine


def main():
    vision = VisionEngine()

    image_path = "sandbox/screenshots/iris_screen.png"

    result = vision.execute(image_path)

    print("Vision result:")
    print(result)


if __name__ == "__main__":
    main()