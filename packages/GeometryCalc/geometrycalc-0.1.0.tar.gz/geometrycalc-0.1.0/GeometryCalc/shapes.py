"""
Calculate geometrical quantities for different shapes
"""
import math


def circle_area(radius):
    """
    Calculate the area of a circle.

    Parameters:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle.
    """
    return math.pi * radius ** 2


def circle_perimeter(radius):
    """
    Calculate the perimeter of a circle.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The perimeter of the circle.
    """
    return 2 * math.pi * radius


def rectangle_area(length, width):
    """
    Calculate the area of a rectangle.

    Args:
        length (int or float): The length of the rectangle.
        width (int or float): The width of the rectangle.

    Returns:
        float: The calculated area of the rectangle.
    """
    return length * width


def rectangle_perimeter(length, width):
    """
    Calculate the perimeter of a rectangle given its length and width.

    Args:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The perimeter of the rectangle.
    """
    return 2 * (length + width)


def triangle_area(base, height):
    """
    Calculates the area of a triangle given its base and height.

    Parameters:
    base (float): The length of the base of the triangle.
    height (float): The height of the triangle.

    Returns:
    float: The area of the triangle.
    """
    return 0.5 * base * height


def triangle_perimeter(side1, side2, side3):
    """
    Calculates the perimeter of a triangle given the lengths of its three sides

    Parameters:
        side1 (float): The length of the first side of the triangle.
        side2 (float): The length of the second side of the triangle.
        side3 (float): The length of the third side of the triangle.

    Returns:
        float: The perimeter of the triangle.
    """
    return side1 + side2 + side3
