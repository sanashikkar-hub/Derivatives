from flask import Flask, render_template, request
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    x, y = sp.symbols('x y')
    curve_input = request.form["curve"]
    x0 = float(request.form["x"])
    y0 = float(request.form["y"])
    curve_eq = sp.sympify(curve_input)

    df_dx = sp.diff(curve_eq, x)
    df_dy = sp.diff(curve_eq, y)
    df_dx_val = df_dx.subs({x: x0, y: y0})
    df_dy_val = df_dy.subs({x: x0, y: y0})

    result = ""
    graph_generated = False

    if df_dy_val != 0:
        tangent_slope = -df_dx_val / df_dy_val
        tangent_eq = df_dx_val * (x - x0) + df_dy_val * (y - y0)
        normal_slope = -1 / tangent_slope
        normal_eq = y - y0 - normal_slope * (x - x0)

        result += f"Slope of Tangent: {tangent_slope}\n"
        result += f"Tangent Line: {sp.Eq(tangent_eq, 0)}\n"
        result += f"Slope of Normal: {normal_slope}\n"
        result += f"Normal Line: {sp.Eq(normal_eq, 0)}\n"
    else:
        result += "Tangent line is vertical.\n"
        result += f"Tangent Line: x = {x0}\n"
        result += f"Normal Line: y = {y0}\n"

    numerator = (df_dx_val**2 + df_dy_val**2)**(3/2)
    d2f_dx2 = sp.diff(df_dx, x).subs({x: x0, y: y0})
    d2f_dy2 = sp.diff(df_dy, y).subs({x: x0, y: y0})
    d2f_dxdy = sp.diff(df_dx, y).subs({x: x0, y: y0})

    denominator = df_dx_val**2 * d2f_dy2 - 2 * df_dx_val * df_dy_val * d2f_dxdy + df_dy_val**2 * d2f_dx2

    if denominator != 0:
        radius = abs(numerator / denominator)
        result += f"\nRadius of Curvature: {radius}\n"
    else:
        result += "\nRadius of curvature is undefined at this point.\n"

    result += "\nMaths Microproject by Sai, Kuldeep, Nikhil and Samruddhi"

    try:
        f_lambdified = sp.lambdify((x, y), curve_eq, "numpy")
        x_vals = np.linspace(x0 - 10, x0 + 10, 400)
        y_vals = np.linspace(y0 - 10, y0 + 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = f_lambdified(X, Y)

        plt.figure(figsize=(6, 6))
        plt.contour(X, Y, Z, levels=[0], colors='blue')
        plt.plot(x0, y0, 'ro', label=f"Point ({x0}, {y0})")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Implicit Curve Plot")
        plt.legend()
        plt.grid(True)

        graph_path = os.path.join("static", "graph.png")
        plt.savefig(graph_path)
        plt.close()
        graph_generated = True
    except Exception as e:
        result += f"\nGraph Error: {str(e)}"

    return render_template("index.html", result=result, graph_generated=graph_generated)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
