import argparse
from PIL import Image
import os


def calculate_new_size(args, image):
    base_width, base_height = image.size[0], image.size[1]
    if args.width and args.height:
        new_width, new_height = int(args.width), int(args.height)
        base_ratio = base_width / float(base_height)
        new_ratio = int(new_width) / float(new_height)
        if base_ratio != new_ratio:
            print("Пропорции нового изображения не совпадают с пропорциями "
                  "исходного изображения!")
        return new_width, new_height
    elif args.width:
        new_width = int(args.width)
        ratio = (new_width / float(base_width))
        new_height = int(base_height * float(ratio))
        return new_width, new_height
    elif args.height:
        new_height = int(args.height)
        ratio = (new_height / float(base_height))
        new_width = int(base_width * float(ratio))
        return new_width, new_height
    if args.scale:
        new_width = int(base_width * float(args.scale))
        new_height = int(base_height * float(args.scale))
        return new_width, new_height


def resize_image(image, new_size):
    new_width, new_height = new_size
    resized_img = image.resize((new_width, new_height), Image.ANTIALIAS)
    return resized_img


def save_resized_image(args, resized_image):
    if not args.output:
        dirname = os.path.dirname(args.path)
        basename = os.path.basename(args.path).split('.')[0]
        fileformat = os.path.basename(args.path).split('.')[1]
        result_width = str(resized_image.size[0])
        result_height = str(resized_image.size[1])
        output = "%s/%s__%sx%s.%s" % (
            dirname, basename, result_width, result_height, fileformat)
    else:
        output = args.output
    resized_image.save(output, resized_image.format)
    return


def test_arguments(args):
    if (args.scale and args.width and args.height) or \
       (args.scale and args.width) or (args.scale and args.height):
        print("Укажите или размер новой картинки или масштаб.\n"
              "Совместное указание этих аргументов недопустимо!")
        return False
    if not (args.scale or args.width or args.height):
        print("Не указано ни одного параметра для изменения "
              "размера изображения!")
        return False
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="путь до исходной картинки")
    parser.add_argument("--width",
                        help="ширина результирующей картинки")
    parser.add_argument("--height",
                        help="высота результирующей картинки")
    parser.add_argument("--scale",
                        help="во сколько раз увеличить изображение")
    parser.add_argument("--output",
                        help="путь для сохранения полученного файл")
    arguments = parser.parse_args()
    if test_arguments(arguments):
        img = Image.open(arguments.path)
        new_size = calculate_new_size(arguments, img)
        new_image = resize_image(img, new_size)
        save_resized_image(arguments, new_image)
