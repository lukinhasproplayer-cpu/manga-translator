from pathlib import Path

# Nome do projeto
projeto = Path("TradutorManga")

# Pastas
pastas = [
    "assets",
    "fonts",
    "models",
    "cache",
    "logs",
    "config",
    "overlay",
    "ocr",
    "translator",
    "capture",
    "render",
    "detector",
    "ui",
]

# Arquivos principais
arquivos = [
    "main.py",
    "settings.py",
    "requirements.txt",
    "README.md",
]

# Criar pasta principal
projeto.mkdir(exist_ok=True)

# Criar subpastas
for pasta in pastas:
    (projeto / pasta).mkdir(parents=True, exist_ok=True)

# Criar arquivos principais
for arquivo in arquivos:
    (projeto / arquivo).touch(exist_ok=True)

# Criar __init__.py em cada módulo
modulos = [
    "overlay",
    "ocr",
    "translator",
    "capture",
    "render",
    "detector",
    "ui",
]

for modulo in modulos:
    (projeto / modulo / "__init__.py").touch(exist_ok=True)

# Arquivos internos

# Capture
(projeto / "capture" / "screen_capture.py").touch(exist_ok=True)

# OCR
(projeto / "ocr" / "ocr_engine.py").touch(exist_ok=True)

# Tradutor
(projeto / "translator" / "translator.py").touch(exist_ok=True)

# Detector
(projeto / "detector" / "balloon_detector.py").touch(exist_ok=True)

# Render
(projeto / "render" / "renderer.py").touch(exist_ok=True)

# Overlay
(projeto / "overlay" / "overlay_window.py").touch(exist_ok=True)

# Interface
(projeto / "ui" / "main_window.py").touch(exist_ok=True)

print("Projeto criado com sucesso!")
print()
print("Estrutura:")
for caminho in projeto.rglob("*"):
    print(caminho)