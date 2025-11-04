import re
import json
import os

ARCHIVO = "estudiantes.json"

# ---------- VALIDACIONES ----------

def validar_carnet(carnet):
    patron = r"^\d{2}-\d{5}-\d$"
    if not re.match(patron, carnet):
        raise ValueError("Carnet inválido. Ejemplo: 25-02395-0")
    return carnet

def validar_estado_civil(estado):  
    opciones = ["soltero", "casado", "divorciado", "viudo"]
    if estado.lower() not in opciones:
        raise ValueError("Estado civil inválido. Opciones: Soltero, Casado, Divorciado, Viudo.")
    return estado.capitalize()

def validar_sexo(sexo):
    if sexo.upper() not in ["M", "F"]:
        raise ValueError("Sexo inválido. Debe ser M o F.")
    return sexo.upper()

def validar_cedula(cedula):
    patron = r"^\d{3}-\d{6}-\d{4}[A-Z]$"
    if not re.match(patron, cedula):
        raise ValueError("Cédula inválida. Ejemplo: 001-123456-0000A")
    return cedula

def validar_anio(anio):
    if not anio.isdigit() or not (1 <= int(anio) <= 6):
        raise ValueError("Año inválido. Debe estar entre 1 y 6.")
    return int(anio)

def validar_nota(nota):
    try:
        nota = float(nota)
        if nota < 0 or nota > 100:
            raise ValueError
    except ValueError:
        raise ValueError("Nota inválida. Debe estar entre 0 y 100.")
    return nota

def validar_ingreso(monto):
    try:
        monto = float(monto)
        if monto < 0:
            raise ValueError
    except ValueError:
        raise ValueError("Monto inválido. Debe ser un número positivo.")
    return monto

# ---------- FUNCIONES DE ARCHIVO ----------

def cargar_estudiantes():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_estudiantes(estudiantes):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(estudiantes, f, ensure_ascii=False, indent=4)

# ---------- FUNCIONES ESTUDIANTE ----------

def registrar_estudiante(estudiantes):
    try:
        print("\n=== REGISTRO DE ESTUDIANTE ===")
        carnet = validar_carnet(input("Carnet (ejemplo 25-02395-0): "))
        nombre = input("Nombre completo: ").title()
        estado_civil = validar_estado_civil(input("Estado civil (Soltero/Casado/Divorciado/Viudo): "))
        sexo = validar_sexo(input("Sexo (M/F): "))
        cedula = validar_cedula(input("Cédula (001-250108-1001B): "))
        direccion = input("Dirección: ").title()
        departamento = input("Departamento: ").title()
        municipio = input("Municipio: ").title()
        area_conocimiento = input("Área de conocimiento: ").title()
        carrera = input("Carrera: ").title()
        anio = validar_anio(input("Año de estudio (1-6): "))
        plan_estudio = input("Plan de estudio: ").upper()
        ingreso_padre = validar_ingreso(input("Ingreso mensual del padre: "))

        notas = []
        print("\n--- Ingreso de notas ---")
        while True:
            materia = input("Nombre de la materia (ENTER para terminar): ").title()
            if materia == "":
                break
            nota = validar_nota(input(f"Ingrese la nota de {materia} (0-100): "))
            notas.append({"materia": materia, "nota": nota})

        estudiantes.append({
            "carnet": carnet,
            "nombre": nombre,
            "estado_civil": estado_civil,
            "sexo": sexo,
            "cedula": cedula,
            "direccion": direccion,
            "departamento": departamento,
            "municipio": municipio,
            "area_conocimiento": area_conocimiento,
            "carrera": carrera,
            "anio": anio,
            "plan_estudio": plan_estudio,
            "ingreso_padre": ingreso_padre,
            "notas": notas
        })

        guardar_estudiantes(estudiantes)
        print(f"\n  Estudiante '{nombre}' registrado correctamente.\n")

    except ValueError as e:
        print(f"\n  Error: {e}\n")

def mostrar_mis_datos(estudiantes):
    carnet = input("\nIngrese su carnet para ver sus datos: ")
    for est in estudiantes:
        if est["carnet"] == carnet:
            print("\n=== MIS DATOS ===")
            print(f"Carnet:           {est['carnet']}")
            print(f"Nombre completo:  {est['nombre']}")
            print(f"Cédula:           {est['cedula']}")
            print(f"Sexo:             {est['sexo']}")
            print(f"Estado civil:     {est['estado_civil']}")
            print(f"Dirección:        {est['direccion']}")
            print(f"Departamento:     {est['departamento']}")
            print(f"Municipio:        {est['municipio']}")
            print(f"Área:             {est['area_conocimiento']}")
            print(f"Carrera:          {est['carrera']}")
            print(f"Año:              {est['anio']}")
            print(f"Plan de estudio:  {est['plan_estudio']}")
            print(f"Ingreso Padre:    C${est['ingreso_padre']:.2f}")
            print("\n--- Notas ---")
            if not est["notas"]:
                print("No tiene notas registradas.")
            else:
                print(f"{'Materia':<25}{'Nota':>10}{'Estado':>15}")
                print("-" * 50)
                for n in est["notas"]:
                    estado = "Aprobado" if n["nota"] >= 60 else "Reprobado"
                    print(f"{n['materia']:<25}{n['nota']:>10.2f}{estado:>15}")
            print("-" * 50)
            return
    print("\nNo se encontró el estudiante.\n")

def calcular_promedio_personal(estudiantes):
    carnet = input("\nIngrese el carnet: ")
    for est in estudiantes:
        if est["carnet"] == carnet:
            if not est["notas"]:
                print("No tiene notas registradas.\n")
                return
            promedio = sum(n["nota"] for n in est["notas"]) / len(est["notas"])
            print(f"\nPromedio de {est['nombre']}: {promedio:.2f}")
            estado = "Aprobado  " if promedio >= 60 else "Reprobado "
            print(f"Estado general: {estado}\n")
            return
    print("\nNo se encontró el estudiante.\n")

# ---------- FUNCIONES PROFESOR ----------

def mostrar_todos(estudiantes):
    print("\n=== LISTA DE ESTUDIANTES REGISTRADOS ===")
    if not estudiantes:
        print("No hay estudiantes registrados.\n")
        return
    print(f"{'CARNET':<15}{'NOMBRE':<30}{'CARRERA':<25}{'PROMEDIO':<10}")
    print("-" * 80)
    for est in estudiantes:
        promedio = sum(n["nota"] for n in est["notas"]) / len(est["notas"]) if est["notas"] else 0
        print(f"{est['carnet']:<15}{est['nombre']:<30}{est['carrera']:<25}{promedio:<10.2f}")
    print("-" * 80 + "\n")

def actualizar_estudiante(estudiantes):
    carnet = input("\nIngrese el carnet del estudiante a actualizar: ")
    for est in estudiantes:
        if est["carnet"] == carnet:
            print(f"\nActualizando datos de {est['nombre']}")
            est['nombre'] = input(f"Nuevo nombre ({est['nombre']}): ").title() or est['nombre']
            est['carrera'] = input(f"Nueva carrera ({est['carrera']}): ").title() or est['carrera']
            opc = input("¿Desea actualizar notas? (S/N): ").upper()
            if opc == "S":
                est['notas'].clear()
                while True:
                    materia = input("Materia (ENTER para terminar): ").title()
                    if materia == "":
                        break
                    nota = validar_nota(input(f"Nota de {materia}: "))
                    est['notas'].append({"materia": materia, "nota": nota})
            guardar_estudiantes(estudiantes)
            print("\n  Datos actualizados correctamente.\n")
            return
    print("\nNo se encontró el estudiante.\n")

def eliminar_estudiante(estudiantes):
    carnet = input("\nIngrese el carnet del estudiante a eliminar: ")
    for i, est in enumerate(estudiantes):
        if est["carnet"] == carnet:
            confirm = input(f"¿Eliminar a {est['nombre']}? (S/N): ").upper()
            if confirm == "S":
                estudiantes.pop(i)
                guardar_estudiantes(estudiantes)
                print("\n  Estudiante eliminado correctamente.\n")
            return
    print("\nNo se encontró el estudiante.\n")

# ---------- FUNCIONES DE PILA / CONFIRMACIÓN ----------

def confirmar_accion(accion):
    pila = []
    while True:
        confirm = input(f"¿Está seguro que desea {accion}? (S/N): ").upper()
        if confirm == "S":
            pila.append(True)   # Guardamos confirmación en la pila
            return True
        elif confirm == "N":
            pila.append(False)
            print("Acción cancelada.\n")
            return False
        else:
            print("Ingrese S para sí o N para no.")

# ---------- MENÚS ----------

def menu_estudiante(estudiantes):
    while True:
        print("\n=== MENÚ ESTUDIANTE ===")
        print("1. Registrar mis datos y notas")
        print("2. Visualizar mis datos y notas")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            if confirmar_accion("registrar sus datos"):
                registrar_estudiante(estudiantes)
        elif opcion == "2":
            if confirmar_accion("ver sus datos"):
                mostrar_mis_datos(estudiantes)
        elif opcion == "3":
            break
        else:
            print("Opción inválida.\n")

def menu_profesor(estudiantes):
    while True:
        print("\n=== MENÚ PROFESOR ===")
        print("1. Ver lista de estudiantes")
        print("2. Actualizar datos de un estudiante")
        print("3. Eliminar estudiante")
        print("4. Calcular promedio de un estudiante")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if confirmar_accion("ver la lista de estudiantes"):
                mostrar_todos(estudiantes)
        elif opcion == "2":
            if confirmar_accion("actualizar datos de un estudiante"):
                actualizar_estudiante(estudiantes)
        elif opcion == "3":
            if confirmar_accion("eliminar un estudiante"):
                eliminar_estudiante(estudiantes)
        elif opcion == "4":
            if confirmar_accion("calcular promedio de un estudiante"):
                calcular_promedio_personal(estudiantes)
        elif opcion == "5":
            break
        else:
            print("Opción inválida.\n")

# ---------- PROGRAMA PRINCIPAL ----------

def main():
    estudiantes = cargar_estudiantes()
    print("✅ Sistema Académico iniciado correctamente.\n")
    while True:
        print("\n=== MENÚ INICIAL ===")
        print("1. Soy estudiante")
        print("2. Soy profesor")
        print("3. Salir")
        rol = input("Seleccione una opción: ")
        if rol == "1":
            menu_estudiante(estudiantes)
        elif rol == "2":
            menu_profesor(estudiantes)
        elif rol == "3":
            print("\nGracias por usar el sistema. ¡Hasta pronto!\n")
            break
        else:
            print("Opción inválida.\n")

if __name__ == "__main__":
    main()
