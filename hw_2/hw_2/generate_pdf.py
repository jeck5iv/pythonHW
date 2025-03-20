from texcellentlatexgenerator.generator import generate_latex
import subprocess
import os

data = [
    ["ID", "Name", "POWER"],
    [1, "Ann", 9],
    [2, "Boris", 30],
    [3, "C. A. T.", 1000000000]
]

image_path = "example.png"
latex_code = generate_latex(data=data, image_path=image_path)

output_tex_path = os.path.join("artifacts", "output.tex")
with open(output_tex_path, "w", encoding="utf-8") as file:
    file.write(latex_code)

try:
    subprocess.run(["pdflatex", "output.tex"], check=True, cwd="artifacts")
    print("PDF успешно сгенерирован: artifacts/output.pdf")
except subprocess.CalledProcessError as e:
    print(f"Ошибка при генерации PDF: {e}")