import math

class BezierCurve:
    def __init__(self, control_points):
        self.control_points = control_points
    
    def _binomial_coefficient(self, n, k):
        # Compute the binomial coefficient n choose k
        return math.factorial(n) // (math.factorial(k) * math.factorial(n-k))
    
    def get_point(self, t):
        # Compute the point on the Bézier curve corresponding to the value of t
        n = len(self.control_points) - 1
        x, y = 0, 0
        for i in range(n+1):
            coeff = self._binomial_coefficient(n, i) * ((1 - t) ** (n-i)) * (t ** i)
            x += coeff * self.control_points[i][0]
            y += coeff * self.control_points[i][1]
        return x, y
    
    def sample_points(self, num_points):
        # Sample points along the Bézier curve and return them as a list of tuples
        return [self.get_point(t / num_points) for t in range(num_points)]


if __name__ =="__main__":
    import matplotlib.pyplot as plt

    # Define the control points for the Bézier curve
    control_points = [(0, 0), (1, 1), (2, -1), (3, 0)]

    # Create a BezierCurve object and sample some points along the curve
    bc = BezierCurve(control_points)
    points = bc.sample_points(100)

    # Plot the sampled points
    x_vals, y_vals = zip(*points)
    plt.plot(x_vals, y_vals)
    plt.show()
