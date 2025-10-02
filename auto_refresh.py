import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def actualizar_pagina(url: str, intervalo_minutos: float = 10.0) -> None:
    """Abre ``url`` en Chrome y la actualiza cada ``intervalo_minutos``.

    Parameters
    ----------
    url:
        Dirección del sitio a vigilar.
    intervalo_minutos:
        Cantidad de minutos entre refrescos consecutivos.
    """
    opciones = Options()
    opciones.add_argument("--headless=new")

    with webdriver.Chrome(options=opciones) as driver:
        driver.get(url)

        intervalo_segundos = intervalo_minutos * 60
        while True:
            time.sleep(intervalo_segundos)
            driver.refresh()
            print("Página actualizada")


if __name__ == "__main__":
    actualizar_pagina(
        "https://campusvirtual.cedsa.edu.ar/postitulo/course/view.php?id=38"
    )
