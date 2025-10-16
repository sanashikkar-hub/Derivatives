from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    x, y = sp.symbols('x y')
    curve_input = request.form["curve"]
    x0 = sp.Rational(request.form["x"])
    y0 = sp.Rational(request.form["y"])
    curve_eq = sp.sympify(curve_input)

    df_dx = sp.diff(curve_eq, x)
    df_dy = sp.diff(curve_eq, y)
    df_dx_val = df_dx.subs({x: x0, y: y0})
    df_dy_val = df_dy.subs({x: x0, y: y0})

    result = ""

    # Tangent and Normal
    if df_dy_val != 0:
        tangent_slope = sp.Rational(-df_dx_val, df_dy_val)
        tangent_eq = df_dx_val * (x - x0) + df_dy_val * (y - y0)
        normal_slope = sp.Rational(-1, tangent_slope)
        normal_eq = y - y0 - normal_slope * (x - x0)

        result += f"Slope of Tangent: {tangent_slope}\n"
        result += f"Tangent Line: {sp.Eq(tangent_eq, 0)}\n"
        result += f"Slope of Normal: {normal_slope}\n"
        result += f"Normal Line: {sp.Eq(normal_eq, 0)}\n"
    else:
        result += "Tangent line is vertical.\n"
        result += f"Tangent Line: x = {x0}\n"
        result += f"Normal Line: y = {y0}\n"

    # Maxima/Minima
    if 'y' not in curve_input:
        f = curve_eq
        f_prime = sp.diff(f, x)
        critical_points = sp.solve(f_prime, x)
        f_double_prime = sp.diff(f_prime, x)

        result += "\nFunction Analysis:\n"
        result += f"f(x) = {f}\n"
        result += f"f'(x) = {f_prime}\n"
        result += f"Critical Points: {critical_points}\n"

        for cp in critical_points:
            concavity = f_double_prime.subs(x, cp)
            nature = "Minimum" if concavity > 0 else "Maximum" if concavity < 0 else "Inflection"
            fx_val = f.subs(x, cp)
            result += f"At x = {cp}, f(x) = {fx_val}, Nature: {nature}\n"

    # Radius of Curvature
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

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

