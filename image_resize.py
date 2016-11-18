import argparse
from PIL import Image
import os


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


def resize_image(args):
    img = Image.open(args.path)
    if args.width and args.height:
        resized_image = resize_with_width_and_height(
            img, int(args.width), int(args.height))
    elif args.width:
        resized_image = resize_with_width(img, int(args.width))
    elif args.height:
        resized_image = resize_with_height(img, int(args.height))
    if args.scale:
        resized_image = resize_with_scale(img, float(args.scale))
    if not args.output:
        dirname = os.path.dirname(args.path)
        basename = os.path.basename(args.path).split('.')[0]
        fileformat = os.path.basename(args.path).split('.')[1]
        result_width = str(resized_image.size[0])
        result_height = str(resized_image.size[1])
        output = dirname + '/' + basename + '__' + result_width + 'x' + result_height + '.' + fileformat
    else:
        output = args.output
    resized_image.save(output, img.format)
    return


def resize_with_width_and_height(image, width, height):
    base_width = image.size[0]
    base_height = image.size[1]
    base_ratio = base_width / float(base_height)
    new_ratio = width / float(height)
    if base_ratio != new_ratio:
        print("Пропорции нового изображения не совпадают с пропорциями "
              "исходного изображения!")
    resized_img = image.resize((width, height), Image.ANTIALIAS)
    return resized_img


def resize_with_height(image, new_height):
    base_height = image.size[1]
    ratio = (new_height / float(base_height))
    new_width = int(image.size[0] * float(ratio))
    resized_img = image.resize(
        (new_width, new_height), Image.ANTIALIAS)
    return resized_img


def resize_with_width(image, new_width):
    base_width = image.size[0]
    ratio = (new_width / float(base_width))
    new_height = int(image.size[1] * float(ratio))
    resized_img = image.resize(
        (new_width, new_height), Image.ANTIALIAS)
    return resized_img


def resize_with_scale(image, scale):
    new_width = int(image.size[0] * scale)
    new_height = int(image.size[1] * scale)
    resized_img = image.resize(
        (new_width, new_height), Image.ANTIALIAS)
    return resized_img


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
        resize_image(arguments)
