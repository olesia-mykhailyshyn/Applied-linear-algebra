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
    print("Матриця точок після трансформації:")
    print(transformed_points)


def rotation(points, angle):
    rotation_matrix = cv2.getRotationMatrix2D((0, 0), angle, 1)
    rotated_points = cv2.transform(np.array([points]), rotation_matrix[:, :2]).squeeze()
    return rotated_points


def scaling(points, object_choice, coefficient):
    if object_choice == 'лисиця':
        points1 = np.float32(points[:3])
    else:
        points1 = np.float32(points[:3])
    scaled_points = points1 * coefficient
    scale_matrix = cv2.getAffineTransform(points1, scaled_points)
    scaled_points = custom_transform(points, scale_matrix)
    return scaled_points


def reflection(points, axis):
    if object_choice == 'лисиця':
        points1 = np.float32(points[:3])
    else:
        points1 = np.float32(points[:3])
    if axis == 'x':
        reflected_points = cv2.transform(np.array([points1]), np.float32([[-1, 0], [0, 1]]))
    else:
        reflected_points = cv2.transform(np.array([points1]), np.float32([[1, 0], [0, -1]]))
    reflection_matrix = cv2.getAffineTransform(points1, reflected_points)
    reflected_points = custom_transform(points, reflection_matrix)
    return reflected_points


def shearing(points, axis, coefficient):
    if object_choice == 'лисиця':
        points1 = np.float32(points[:3])
    else:
        points1 = np.float32(points[:3])
    if axis == 'x':
        sheared_points = cv2.transform(np.array([points1]), np.float32([[1, 0], [coefficient, 1]]))
    else:
        sheared_points = cv2.transform(np.array([points1]), np.float32([[1, coefficient], [0, 1]]))
    sheared_matrix = cv2.getAffineTransform(points1, sheared_points)
    sheared_points = custom_transform(points, sheared_matrix)
    return sheared_points


def custom_transform(points, transformation_matrix):
    transformed_points = cv2.transform(np.array([points]), transformation_matrix).squeeze()
    return transformed_points


def rotate_image(image, angle):
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
    return rotated_image


def scale_image(image, coefficient):
    height, width = image.shape[:2]
    old_dim = (width, height)
    new_width = int(width * coefficient)
    new_height = int(height * coefficient)
    new_dim = (new_width, new_height)
    scaled_image = cv2.resize(image, new_dim, interpolation=cv2.INTER_LINEAR)
    return scaled_image, old_dim, new_dim


def reflect_image(image, axis):
    if axis == 'x':
        reflected_image = cv2.flip(image, 0)
    else:
        reflected_image = cv2.flip(image, 1)
    return reflected_image


def select_object(object_choice):
    if object_choice == 'лисиця':
        return fox.copy(), fox.copy()
    elif object_choice == 'собака':
        return dog.copy(), dog.copy()
    else:
        image_path = r'image2.png'
        image = cv2.imread(image_path)
        return image, image


while True:
    command = input("\nВведіть команду (обертати/маштабувати/відзеркалювати/нахил/універсальна/вихід): ").strip().lower()
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
            current_points = rotation(current_points, angle)


    elif command == 'маштабувати':
        coefficient = float(input("Введіть коефіцієнт масштабування (k>1 для збільшення, 0<k<1 для зменшення): "))
        if object_choice == 'зображення':
            current_image, old_dim, new_dim = scale_image(current_image, coefficient)
            print(f"Розмір зображення змінився з {old_dim} на {new_dim}")
        else:
            current_points = scaling(current_points, object_choice, coefficient)

    elif command == 'відзеркалювати':
        axis = input("Введіть вісь відображення ('x' або 'y'): ").strip().lower()
        if object_choice == 'зображення':
            current_image = reflect_image(current_image, axis)
        else:
            current_points = reflection(current_points, axis)

    elif command == 'нахил':
        axis = input("Введіть вісь нахилу ('x' або 'y'): ").strip().lower()
        coefficient = float(input("Введіть коефіцієнт нахилу: "))
        current_points = shearing(current_points, axis, coefficient)

    elif command == 'універсальна':
        print("Введіть кастомну матрицю трансформації: ")
        transformation_matrix = np.zeros((2, 2))
        for i in range(2):
            for j in range(2):
                transformation_matrix[i, j] = float(input(f"Елемент [{i}, {j}]: "))
        current_points = custom_transform(current_points, transformation_matrix)
    else:
        print("Невідома команда. Будь ласка, введіть одну з доступних команд.")

    if object_choice != 'зображення':
        visualize_transform(original_points, current_points, f'{object_choice.capitalize()} - {command.capitalize()}')
    else:
        plt.imshow(cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB))
        plt.title(f"Трансформація зображення - {command.capitalize()}")
        plt.axis('off')
        plt.show()