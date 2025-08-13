import pytest
import importlib

def try_import(module_name, func_name):
    """
    Intenta importar un módulo y obtener la función especificada.
    Si falla, el test se marcará como SKIPPED en lugar de romper toda la ejecución.
    """
    try:
        module = importlib.import_module(module_name)
        return getattr(module, func_name)
    except (ModuleNotFoundError, AttributeError):
        pytest.skip(f"Módulo o función no encontrada: {module_name}.{func_name}")


# ======================================================
# PARTE A — Condicionales (if / if-else / elif)
# ======================================================

@pytest.mark.parametrize("n, esperado", [
    (5, "positivo"),
    (0, None),
    (-3, None),
])
def test_usar_if(n, esperado):
    func = try_import("ejemplo_if", "usar_if")
    assert func(n) == esperado


@pytest.mark.parametrize("n, esperado", [
    (10, "par"),
    (7, "impar"),
    (0, "par"),
])
def test_usar_if_else(n, esperado):
    func = try_import("ejemplo_if_else", "usar_if_else")
    assert func(n) == esperado


@pytest.mark.parametrize("n, esperado", [
    (4, "positivo"),
    (0, "cero"),
    (-1, "negativo"),
])
def test_clasificar_numero(n, esperado):
    func = try_import("ejemplo_elif", "clasificar_numero")
    assert func(n) == esperado


# ======================================================
# PARTE B — Ciclos (for / while)
# ======================================================

@pytest.mark.parametrize("nums, esperado", [
    ([1, 2, 3, 4], 10),
    ([0, 0, 0], 0),
    ([5], 5),
])
def test_sumar_lista(nums, esperado):
    func = try_import("sumar_for", "sumar_lista")
    assert func(nums) == esperado


@pytest.mark.parametrize("n, esperado", [
    (3, [3, 2, 1, 0]),
    (0, [0]),
    (5, [5, 4, 3, 2, 1, 0]),
])
def test_contar_descendente(n, esperado):
    func = try_import("contar_while", "contar_descendente")
    assert func(n) == esperado


# ======================================================
# PARTE C — Buscaminas (matrices y lógica)
# ======================================================

def test_crear_tablero_dim_y_valor():
    func = try_import("crear_tablero", "crear_tablero")
    t = func(3, 4, 9)
    assert isinstance(t, list)
    assert len(t) == 3 and all(len(f) == 4 for f in t)
    assert all(all(c == 9 for c in f) for f in t)

def test_crear_tablero_filas_independientes():
    func = try_import("crear_tablero", "crear_tablero")
    t = func(2, 2, 0)
    t[0][0] = 1
    assert t[1][0] == 0, "Cada fila debe ser una lista independiente (no aliasing)."

def test_colocar_minas_basico():
    func_ct = try_import("crear_tablero", "crear_tablero")
    func = try_import("colocar_minas", "colocar_minas")
    base = func_ct(3, 3, 0)
    m = func(base, [(0, 0), (2, 1)])
    assert m[0][0] == -1
    assert m[2][1] == -1
    # celdas sin mina siguen con 0
    assert m[0][1] == 0 and m[1][1] == 0 and m[2][2] == 0

def test_colocar_minas_fuera_de_rango_se_ignoran():
    func_ct = try_import("crear_tablero", "crear_tablero")
    func = try_import("colocar_minas", "colocar_minas")
    base = func_ct(2, 2, 0)
    m = func(base, [(-1, 0), (0, -1), (5, 5), (1, 1)])
    assert m[1][1] == -1
    assert m[0][0] == 0 and m[0][1] == 0 and m[1][0] == 0

def test_calcular_numeros_conserva_minas_y_cuentas_correctas():
    func_ct = try_import("crear_tablero", "crear_tablero")
    func_cm = try_import("colocar_minas", "colocar_minas")
    func = try_import("calcular_numeros", "calcular_numeros")
    base = func_ct(3, 3, 0)
    minas = func_cm(base, [(0, 0), (2, 1)])
    nums = func(minas)
    # minas permanecen como -1
    assert nums[0][0] == -1 and nums[2][1] == -1
    # conteo de (1,1) debe ser 2 (adyacente a dos minas)
    assert nums[1][1] == 2
    # esquina opuesta a las minas debería ser 0
    assert nums[0][2] == 0

def test_inicializar_visible():
    func = try_import("inicializar_visible", "inicializar_visible")
    v = func(2, 3)
    assert v == [[False, False, False], [False, False, False]]

def test_revelar_celda_sin_mina_numero():
    func_rc = try_import("revelar_celda", "revelar_celda")
    func_ct = try_import("crear_tablero", "crear_tablero")
    func_cm = try_import("colocar_minas", "colocar_minas")
    func_cn = try_import("calcular_numeros", "calcular_numeros")
    func_v = try_import("inicializar_visible", "inicializar_visible")

    base = func_ct(3, 3, 0)
    minas = func_cm(base, [(0, 0), (2, 1)])
    nums = func_cn(minas)
    vis = func_v(3, 3)

    vis, golpe = func_rc(minas, nums, vis, 1, 1)  # valor 2
    assert golpe is False
    assert vis[1][1] is True
    # no se expanden ceros porque no es 0
    total_visibles = sum(sum(1 for c in fila if c) for fila in vis)
    assert total_visibles == 1

def test_revelar_celda_con_mina():
    func_rc = try_import("revelar_celda", "revelar_celda")
    func_ct = try_import("crear_tablero", "crear_tablero")
    func_cm = try_import("colocar_minas", "colocar_minas")
    func_cn = try_import("calcular_numeros", "calcular_numeros")
    func_v = try_import("inicializar_visible", "inicializar_visible")

    base = func_ct(2, 2, 0)
    minas = func_cm(base, [(0, 0)])
    nums = func_cn(minas)
    vis = func_v(2, 2)

    vis, golpe = func_rc(minas, nums, vis, 0, 0)
    assert golpe is True
    assert vis[0][0] is True
    # las otras celdas siguen ocultas
    assert vis[0][1] is False and vis[1][0] is False and vis[1][1] is False

def test_revelar_celda_expansion_cero():
    func_rc = try_import("revelar_celda", "revelar_celda")
    func_ct = try_import("crear_tablero", "crear_tablero")
    func_cm = try_import("colocar_minas", "colocar_minas")
    func_cn = try_import("calcular_numeros", "calcular_numeros")
    func_v = try_import("inicializar_visible", "inicializar_visible")

    base = func_ct(3, 3, 0)
    minas = func_cm(base, [(0, 0)])     # solo una mina en (0,0)
    nums = func_cn(minas)
    vis = func_v(3, 3)

    vis, golpe = func_rc(minas, nums, vis, 2, 2)  # celda 0; debe expandir
    assert golpe is False
    # deben revelarse todas las no-minas (8 celdas)
    total_visibles = sum(sum(1 for c in fila if c) for fila in vis)
    assert total_visibles == 8
    assert vis[0][0] is False  # la mina sigue oculta

def test_checar_victoria_true_y_false():
    func_cv = try_import("checar_victoria", "checar_victoria")
    func_ct = try_import("crear_tablero", "crear_tablero")
    func_cm = try_import("colocar_minas", "colocar_minas")
    func_cn = try_import("calcular_numeros", "calcular_numeros")
    func_v  = try_import("inicializar_visible", "inicializar_visible")
    func_rc = try_import("revelar_celda", "revelar_celda")

    # Caso False: 2x2, sin revelar nada aún
    base = func_ct(2, 2, 0)
    minas = func_cm(base, [(0, 0)])
    nums = func_cn(minas)
    vis  = func_v(2, 2)
    assert func_cv(minas, vis) is False

    # Caso True: 3x3, una mina en (0,0); revelar (2,2) (valor 0) expande todo lo no-mina
    base2 = func_ct(3, 3, 0)
    minas2 = func_cm(base2, [(0, 0)])
    nums2 = func_cn(minas2)
    vis2  = func_v(3, 3)
    vis2, _ = func_rc(minas2, nums2, vis2, 2, 2)
    assert func_cv(minas2, vis2) is True


def test_formatear_tablero_basico_y_mostrar_minas():
    func_ft = try_import("formatear_tablero", "formatear_tablero")
    func_ct = try_import("crear_tablero", "crear_tablero")
    func_cm = try_import("colocar_minas", "colocar_minas")
    func_cn = try_import("calcular_numeros", "calcular_numeros")
    func_v = try_import("inicializar_visible", "inicializar_visible")

    base = func_ct(2, 2, 0)
    minas = func_cm(base, [(0, 1)])
    nums = func_cn(minas)
    vis = func_v(2, 2)

    # sin revelar casi nada: debe haber '#'
    s1 = func_ft(nums, vis)
    assert isinstance(s1, str)
    assert "#" in s1

    # mostrar minas explícitamente
    vis = [[True, True], [True, True]]
    s2 = func_ft(nums, vis, mostrar_minas=True)
    assert "*" in s2  # se deben ver las minas
