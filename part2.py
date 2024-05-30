import cv2
import numpy as np
import matplotlib.pyplot as plt

fox = np.array([[-3, 0], [-2, 1], [3, 1], [3, 2], [5, 5], [5, 3], [6, 2], [7, 2], [7, 1.5], [5, 0], [4, 0],
                [4, -1.5], [3, -1], [3, -1.5], [4, -2.5], [4.5, -2.5], [3.5, -3], [2, -1.5], [2, -1], [-2, -2],
                [-2, -2.5], [-1, -2.5], [-1, -3], [-3, -3], [-3, -2], [-2, -1], [-3, -1], [-4, -2], [-7, -2],
                [-8, -1], [-7, 0], [-3, 0]])

dog = np.array([[1, -3], [2, -3], [3, -2], [3, 3], [4, 3], [5, 4], [5, 6], [4, 7], [3, 7], [2, 6], [3, 5], [3, 5.5],
                [4, 5], [3, 4], [2, 5], [-3, 5], [-4, 6], [-4, 9], [-5, 10], [-5, 11], [-6, 10], [-7, 10], [-7, 10],
                [-7, 8], [-9, 8], [-9, 7], [-8, 6], [-6, 6], [-7, 3], [-6, 2], [-6, -1], [-7, -2], [-7, -3],
                [-6, -3], [-4, -2], [-4, 2], [1, 2], [2, -1], [1, -2], [1, -3]])


def rotate(points, angle):
    center = (0, 0)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_points = cv2.transform(np.array([points]), rotation_matrix).squeeze()
    return rotated_points


def scale(points, scale_factor):
    scaled_points = points * scale_factor
    return scaled_points


def reflect(points, axis):
    if axis == 'x':
        reflection_matrix = np.array([[1, 0], [0, -1]], dtype=np.float32)
    else:
        reflection_matrix = np.array([[-1, 0], [0, 1]], dtype=np.float32)
    reflected_points = cv2.transform(np.array([points]), reflection_matrix).squeeze()
    return reflected_points


def shear(points, axis, shear_angle):
    shear_matrix = np.float32([[1, np.tan(np.radians(shear_angle))],
                               [np.tan(np.radians(shear_angle)), 1]])
    if axis == 'x':
        shear_matrix[1, 0] = 0
    else:
        shear_matrix[0, 1] = 0
    sheared_points = cv2.transform(np.array([points]), shear_matrix).squeeze()
    return sheared_points


def custom_transform(points, transformation_matrix):
    custom_matrix = np.array(transformation_matrix, dtype=np.float32)
    transformed_points = cv2.transform(np.array([points]), custom_matrix).squeeze()
    return transformed_points


def visualize_transform(original_points, transformed_points, title):
    fig, ax = plt.subplots()
    ax.plot(original_points[:, 0], original_points[:, 1], marker='o', color='b', label='Оригінальна')
    ax.fill(original_points[:, 0], original_points[:, 1], alpha=0.3, color='b')
    ax.plot(transformed_points[:, 0], transformed_points[:, 1], marker='o', color='r', label='Трансформована')
    ax.fill(transformed_points[:, 0], transformed_points[:, 1], alpha=0.3, color='r')
    ax.set_title(title)
    ax.set_xlabel('Вісь X')
    ax.set_ylabel('Вісь Y')
    ax.grid(True)
    ax.axis('equal')
    ax.legend()
    plt.show()


def rotate_image(image, angle):
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
    return rotated_image


def scale_image(image, scale_factor):
    scaled_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    return scaled_image


def reflect_image(image, axis):
    if axis == 'x':
        reflected_image = cv2.flip(image, 0)
    else:
        reflected_image = cv2.flip(image, 1)
    return reflected_image


def shear_image(image, axis, shear_angle):
    shear_angle_rad = np.radians(shear_angle)
    if axis == 'x':
        shear_matrix = np.array([[1, np.tan(shear_angle_rad), 0],
                                 [0, 1, 0]], dtype=np.float32)
    else:
        shear_matrix = np.array([[1, 0, 0],
                                 [np.tan(shear_angle_rad), 1, 0]], dtype=np.float32)

    sheared_image = cv2.warpAffine(image, shear_matrix, (image.shape[1], image.shape[0]))
    return sheared_image


def select_object(object_choice):
    if object_choice == 'лисиця':
        return fox.copy(), fox.copy()
    elif object_choice == 'собака':
        return dog.copy(), dog.copy()
    else:
        image_path = r"image.png"
        image = cv2.imread(image_path)
        return image, image


while True:
    command = input(
        "\nВведіть команду (обертати/маштабувати/відзеркалювати/нахил/універсальна/вихід): ").strip().lower()
    if command == 'вихід':
        print("Програма завершена.")
        break

    object_choice = input("Виберіть об'єкт (лисиця/собака/зображення): ").strip().lower()

    original_points, current_points = select_object(object_choice)

    if object_choice == 'зображення':
        original_image = original_points.copy()
        current_image = current_points.copy()
    else:
        original_image = None
        current_image = None

    if command == 'обертати':
        angle = float(input("Введіть кут обертання в градусах: "))
        if object_choice == 'зображення':
            current_image = rotate_image(current_image, angle)
        else:
            current_points = rotate(current_points, angle)

    elif command == 'маштабувати':
        scale_factor = float(input("Введіть коефіцієнт масштабування (>1 для збільшення, <1 для зменшення): "))
        scale_factor = float(input("Введіть коефіцієнт масштабування (>1 для збільшення, <1 для зменшення): "))
        if object_choice == 'зображення':
            current_image = scale_image(current_image, scale_factor)
        else:
            current_points = scale(current_points, scale_factor)

    elif command == 'відзеркалювати':
        axis = input("Введіть вісь відображення ('x' або 'y'): ").strip().lower()
        if object_choice == 'зображення':
            current_image = reflect_image(current_image, axis)
        else:
            current_points = reflect(current_points, axis)

    elif command == 'нахил':
        axis = input("Введіть вісь нахилу ('x' або 'y'): ").strip().lower()
        shear_angle = float(input("Введіть кут нахилу в градусах: "))
        if object_choice == 'зображення':
            current_image = shear_image(current_image, axis, shear_angle)
        else:
            current_points = shear(current_points, axis, shear_angle)

    elif command == 'універсальна':
        transformation_matrix = []
        for i in range(2):
            row = input(f"Введіть рядок матриці трансформації #{i + 1} (через пробіл): ").strip().split()
            transformation_matrix.append([float(num) for num in row])
        if object_choice == 'зображення':
            current_image = custom_transform(current_image, transformation_matrix)
        else:
            current_points = custom_transform(current_points, transformation_matrix)

    else:
        print("Невідома команда. Будь ласка, введіть одну з доступних команд.")

    if object_choice != 'зображення':
        visualize_transform(original_points, current_points, f"Трансформація об'єкту {object_choice.capitalize()}")
    else:
        plt.imshow(cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB))
        plt.title(f"Трансформація зображення {object_choice.capitalize()}")
        plt.axis('off')
        plt.show()