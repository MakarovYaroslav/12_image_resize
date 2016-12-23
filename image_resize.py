import argparse
from PIL import Image
import os


def calculate_new_size(width, height, image):
    base_width, base_height = image.size
    if width and height:
        new_width, new_height = int(width), int(height)
        return new_width, new_height
    elif width:
        new_width = int(width)
        ratio = (new_width / float(base_width))
        new_height = int(base_height * float(ratio))
        return new_width, new_height
    elif height:
        new_height = int(height)
        ratio = (new_height / float(base_height))
        new_width = int(base_width * float(ratio))
        return new_width, new_height


def calculate_new_size_with_scale(scale, image):
    base_width, base_height = image.size
    new_width = int(base_width * scale)
    new_height = int(base_height * scale)
    return new_width, new_height


def if_proportions_mismatch(base_size, new_size):
    base_width, base_height = base_size
    new_width, new_height = new_size
    base_proportion = base_width / float(base_height)
    new_proportion = int(new_width) / float(new_height)
    return base_proportion != new_proportion


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
        return False
    if not (args.scale or args.width or args.height):
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
    args = parser.parse_args()
    if test_arguments(args):
        img = Image.open(args.path)
        if args.scale:
            new_size = calculate_new_size_with_scale(float(args.scale), img)
        else:
            new_size = calculate_new_size(args.width, args.height, img)
            if if_proportions_mismatch(img.size, new_size):
                print("Пропорции нового изображения не совпадают с пропорциями"
                      " исходного изображения!")
        new_image = resize_image(img, new_size)
        save_resized_image(args, new_image)
    else:
        print("Ошибка! Проверьте корректность ввода аргументов.\n"
              "Для вызова справки введите команду 'python3 image_resize.py -h'")
