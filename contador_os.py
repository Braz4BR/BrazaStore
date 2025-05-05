import os

def obter_proxima_os():
    caminho = "contador_os.txt"
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            numero_atual = int(f.read().strip())
    else:
        numero_atual = 0000  # Valor inicial se o arquivo não existir

    proxima_os = numero_atual + 1

    with open(caminho, "w") as f:
        f.write(str(proxima_os))

    return proxima_os
