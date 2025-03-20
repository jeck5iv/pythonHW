from latex_generator_project.latex_generator.latex_generator import generate_latex

data = [
    ["ID", "Name", "POWER"],
    [1, "Ann", 9],
    [2, "Boris", 30],
    [3, "C. A. T.", 1000000000]
]

image_path = "example.png"

latex_code = generate_latex(data=data, image_path=image_path)

with open("artifacts/generated_file.tex", "w", encoding="utf-8") as file:
    file.write(latex_code)

print("Файл artifacts/generated_file.tex создан успешно")