import matplotlib.pyplot as plt
import numpy as np

fox = np.array([[-3, 0], [-2, 1], [3, 1], [3, 2], [5, 5], [5, 3], [6, 2], [7, 2], [7, 1.5], [5, 0], [4, 0],
                [4, -1.5], [3, -1], [3, -1.5], [4, -2.5], [4.5, -2.5], [3.5, -3], [2, -1.5], [2, -1], [-2, -2],
                [-2, -2.5], [-1, -2.5], [-1, -3], [-3, -3], [-3, -2], [-2, -1], [-3, -1], [-4, -2], [-7, -2],
                [-8, -1], [-7, 0], [-3, 0]])

dog = np.array([[1, -3], [2, -3], [3, -2], [3, 3], [4, 3], [5, 4], [5, 6], [4, 7], [3, 7], [2, 6], [3, 5], [3, 5.5],
                [4, 5], [3, 4], [2, 5], [-3, 5], [-4, 6], [-4, 9], [-5, 10], [-5, 11], [-6, 10], [-7, 10], [-7, 10],
                [-7, 8], [-9, 8], [-9, 7], [-8, 6], [-6, 6], [-7, 3], [-6, 2], [-6, -1], [-7, -2], [-7, -3],
                [-6, -3], [-4, -2], [-4, 2], [1, 2], [2, -1], [1, -2], [1, -3]])


def visualisation(points1, points2, title, ax, color1='b', color2='r', alpha=0.3):
    ax.plot(points1[:, 0], points1[:, 1], marker='o', color=color1, label='Оригінальна') #points1[:, 0] - x, points1[:, 1] - y
    ax.fill(points1[:, 0], points1[:, 1], alpha=alpha, color=color1)
    ax.plot(points2[:, 0], points2[:, 1], marker='o', color=color2, label='Трансформована')
    ax.fill(points2[:, 0], points2[:, 1], alpha=alpha, color=color2)
    ax.set_title(title)
    ax.set_xlabel('Вісь X')
    ax.set_ylabel('Вісь Y')
    ax.grid(True)
    ax.axis('equal') #однаковий масштаб
    ax.legend()


def rotation(points, angle):
    angle = np.radians(angle)
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    points_transposed = points.T
    return np.dot(rotation_matrix, points_transposed).T #проти годинникової стрілки
    #return np.dot(points, rotation_matrix)


def scaling(points, coefficient):
    return points * coefficient


def reflection(points, axis):
    if axis == 'x':
        reflection_matrix = np.array([[-1, 0],
                                      [0, 1]])
    else:
        reflection_matrix = np.array([[1, 0],
                                      [0, -1]])
    #return np.dot(points, reflection_matrix)
    return np.dot(reflection_matrix, points.T).T


def shearing(points, axis, coefficient):
    #angle = np.radians(angle)
    # np.tan(angle)
    if axis == 'x':
        shearing_matrix = np.array([[1, 0],
                                    [coefficient, 1]])
    else:
        shearing_matrix = np.array([[1, coefficient],
                                    [0, 1]])
    return np.dot(shearing_matrix, points.T).T


def custom_transform(points, transformation_matrix):
    return np.dot(transformation_matrix, points.T).T


def display_result(original_points, transformed_points, title):
    fig, ax = plt.subplots() #створення фігури
    visualisation(original_points, transformed_points, title, ax) #візуалізація фігури
    plt.show()
    print("Матриця точок після трансформації:")
    print(transformed_points)


current_points_fox = fox.copy()
current_points_dog = dog.copy()

while True:
    command = input("\nВведіть команду (обертати/маштабувати/відзеркалювати/нахил/універсальна/вихід): ").strip().lower()
    if command == 'вихід':
        print("Програма завершена.")
        break

    object_choice = input("Виберіть об'єкт (лисиця/собака): ").strip().lower()

    if object_choice == 'лисиця':
        current_points = current_points_fox
        original_points = fox
    elif object_choice == 'собака':
        current_points = current_points_dog
        original_points = dog
    else:
        print("Невідомий об'єкт. Спробуйте ще раз.")
        continue

    if command == 'обертати':
        angle = float(input("Введіть кут обертання в градусах: "))
        current_points = rotation(current_points, angle)
    elif command == 'маштабувати':
        coefficient = float(input("Введіть коефіцієнт масштабування (k>1 для збільшення, 0>k<1 для зменшення): "))
        current_points = scaling(current_points, coefficient)
    elif command == 'відзеркалювати':
        axis = input("Введіть вісь відзеркалення (x або y): ").strip().lower()
        current_points = reflection(current_points, axis)
    elif command == 'нахил':
        axis = input("Введіть ось для нахилу (x або y): ").strip().lower()
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
        print("Невідома команда. Спробуйте ще раз.")
        continue

    display_result(original_points, current_points, f'{object_choice.capitalize()} - {command.capitalize()}')