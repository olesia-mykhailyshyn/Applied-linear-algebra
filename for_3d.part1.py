import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

cube = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])


def visualisation_3d(points1, points2, title, ax, color1='b', color2='r', alpha=0.3):
    # створення граней куба. кожна грань цу список 4 вершин
    vertices1 = [[points1[0], points1[1], points1[2], points1[3]],
                 [points1[4], points1[5], points1[6], points1[7]],
                 [points1[0], points1[1], points1[5], points1[4]],
                 [points1[2], points1[3], points1[7], points1[6]],
                 [points1[1], points1[2], points1[6], points1[5]],
                 [points1[4], points1[7], points1[3], points1[0]]]

    vertices2 = [[points2[0], points2[1], points2[2], points2[3]],
                 [points2[4], points2[5], points2[6], points2[7]],
                 [points2[0], points2[1], points2[5], points2[4]],
                 [points2[2], points2[3], points2[7], points2[6]],
                 [points2[1], points2[2], points2[6], points2[5]],
                 [points2[4], points2[7], points2[3], points2[0]]]

    # додавання граней куба на графік
    for face in vertices1:
        ax.add_collection3d(Poly3DCollection([face], color=color1, alpha=alpha))
    for face in vertices2:
        ax.add_collection3d(Poly3DCollection([face], color=color2, alpha=alpha))

    ax.set_title(title)
    ax.set_xlabel('Вісь X')
    ax.set_ylabel('Вісь Y')
    ax.set_zlabel('Вісь Z')
    ax.grid(True)

    # обчислення лімітів осей для візуалізації
    all_points = np.concatenate((points1, points2))
    max_range = np.array([all_points[:, 0].max() - all_points[:, 0].min(),
                          all_points[:, 1].max() - all_points[:, 1].min(),
                          all_points[:, 2].max() - all_points[:, 2].min()]).max() / 2.0

    mid_x = (all_points[:, 0].max() + all_points[:, 0].min()) * 0.5
    mid_y = (all_points[:, 1].max() + all_points[:, 1].min()) * 0.5
    mid_z = (all_points[:, 2].max() + all_points[:, 2].min()) * 0.5

    # встановлення лімітів осей
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # створення та додавання легенди
    custom_lines = [plt.Line2D([0], [0], color=color1, lw=4),
                    plt.Line2D([0], [0], color=color2, lw=4)]
    ax.legend(custom_lines, ['Оригінальна', 'Трансформована'])


def rotation_3d(points, axis, angle):
    angle = np.radians(angle)
    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]])
    elif axis == 'y':
        rotation_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]])
    else:
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])
    return np.dot(rotation_matrix, points.T).T


def scaling_3d(points, coefficient):
    return points * coefficient


def reflection_3d(points, plane):
    if plane == 'xy':
        reflection_matrix = np.array([[1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, -1]])
    elif plane == 'yz':
        reflection_matrix = np.array([[-1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]])
    else:
        reflection_matrix = np.array([[1, 0, 0],
                                      [0, -1, 0],
                                      [0, 0, 1]])
    return np.dot(reflection_matrix, points.T).T


def custom_transform_3d(points, transformation_matrix):
    return np.dot(transformation_matrix, points.T).T


def display_result_3d(original_points, transformed_points, title):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    visualisation_3d(original_points, transformed_points, f'{title}', ax, color1='b', color2='r')
    plt.show()


current_points_cube = cube.copy()

while True:
    command = input("\nВведіть команду (обертати/маштабувати/відзеркалювати/універсальна/вихід): ").strip().lower()

    current_points = current_points_cube

    if command == 'обертати':
        axis = input("Введіть вісь обертання ('x', 'y' або 'z'): ").strip().lower()
        angle = float(input("Введіть кут обертання в градусах: "))
        current_points = rotation_3d(current_points, axis, angle)
    elif command == 'маштабувати':
        coefficient = float(input("Введіть коефіцієнт масштабування (k>1 для збільшення, 0>k<1 для зменшення): "))
        current_points = scaling_3d(current_points, coefficient)
    elif command == 'відзеркалювати':
        plane = input("Введіть площину відзеркалення ('xy', 'yz' або 'zx'): ").strip().lower()
        current_points = reflection_3d(current_points, plane)
    elif command == 'універсальна':
        print("Введіть кастомну матрицю трансформації 3x3:")
        transformation_matrix = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                transformation_matrix[i, j] = float(input(f"Елемент [{i}, {j}]: "))
        current_points = custom_transform_3d(current_points, transformation_matrix)
    elif command == 'вихід':
        print("Програма завершена.")
        break
    else:
        print("Невідома команда. Спробуйте ще раз.")
        continue

    display_result_3d(cube, current_points, f'Куб - {command.capitalize()}')