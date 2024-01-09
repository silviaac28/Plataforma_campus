import json


def registrar_camper():
    nuevoCamper = {}
    nuevoCamper["no_id"] = int(input("Ingrese el ID del estudiante: "))

    file = "object.json"
    with open(file, "r") as campers_file:
        users = json.load(campers_file)
    for camper in users:
        if camper["no_id"] == nuevoCamper["no_id"]:
            print("Este estudiante ya se encuentra registrado.")
            return
    nuevoCamper["nombre"] = input("Ingrese el nombre del estudiante: ")
    nuevoCamper["apellidos"] = input("Ingrese los apellidos del estudiante: ")
    nuevoCamper["direccion"] = input("Ingrese la dirección del estudiante: ")
    nuevoCamper["no_celular"] = int(input("Ingrese el No. de celular del estudiante: "))
    nuevoCamper["no_fijo"] = int(input("Ingrese el No. fijo del estudiante: "))
    nuevoCamper["acudiente"] = input("Ingrese el nombre del acudiente: ")
    nuevoCamper["estado"] = "Inscrito"
    users.append(nuevoCamper)
    with open(file, "w") as campers_file:
        json.dump(users, campers_file, indent=4)

    print("El estudiante ha sido registrado exitosamente.")


def visualizar_camper():
    with open("object.json", "r") as file:
        users = json.load(file)
    for user in users:
        print(
            "ID:",
            user["no_id"],
            "Nombre:",
            user["nombre"],
            user["apellidos"],
            " Teléfono:",
            user["no_celular"],
            " Acudiente:",
            user["acudiente"],
            " Estado:",
            user["estado"],
        )
    file.close()


def registrar_prueba():
    with open("object.json", "r+") as campers_file:
        users = json.load(campers_file)
        id = int(
            input("\nIngrese el ID del estudiante del cual desea registrar prueba: ")
        )
        student_found = False
        for user in users:
            if id == user["no_id"]:
                student_found = True
                if user["estado"] == "Aprobado":
                    print(
                        "\nYa se han registrado resultados de prueba de ingreso para este estudiante."
                    )
                else:
                    print(
                        "Usted ha seleccionado el estudiante",
                        user["nombre"],
                        user["apellidos"],
                    )
                    nota_teorica = float(
                        input("Ingrese la nota teórica del estudiante: ")
                    )
                    nota_practica = float(
                        input("Ingrese la nota práctica del estudiante: ")
                    )
                    n_final = (nota_practica + nota_teorica) / 2
                    if n_final >= 60:
                        user["estado"] = "Aprobado"
                        print(f"El estudiante {user['nombre']} ha sido APROBADO.")
                    else:
                        user["estado"] = "NO aprobado"
                        print(f"El estudiante {user['nombre']} ha sido REPROBADO.")
                break

        if not student_found:
            print("Estudiante no encontrado.")
        campers_file.seek(0)
        json.dump(users, campers_file, indent=4)


def asignar_rutas():
    with open("object.json", "r") as f:
        campers_file = json.load(f)
    with open("rutasf.json", "r") as f:
        rutas_file = json.load(f)

    campers_aprobados = [
        camper for camper in campers_file if camper["estado"] == "Aprobado"
    ]

    for camper in campers_aprobados:
        id_camper = camper["no_id"]

        # ESTO REVISA si el ID ya está presente en alguna ruta
        id_presente = any(id_camper in ruta["campers"] for ruta in rutas_file.values())

        if not id_presente:
            id_ruta = None
            for key, ruta in rutas_file.items():
                if len(ruta["campers"]) < 33 and id_camper not in ruta["campers"]:
                    id_ruta = key
                    break

            if id_ruta is not None:
                rutas_file[id_ruta]["campers"].append(id_camper)
                for estudiante in campers_file:
                    if estudiante["no_id"] == camper["no_id"]:
                        estudiante["id_ruta"] = id_ruta
                        estudiante["trainer"] = ruta["trainer"]
                        estudiante["ruta"] = ruta["ruta"]
                        break

    with open("rutasf.json", "w") as f:
        json.dump(rutas_file, f, indent=2)
    with open("object.json", "w") as f:
        json.dump(campers_file, f, indent=2)
    print("Se han asignado automáticamente las rutas para los campers.")


def visualizar_matricula():
    with open("rutasf.json", "r") as f:
        rutas_file = json.load(f)

    for key, ruta in rutas_file.items():
        print(f"\nINFORMACIÓN RUTA {key}:")
        print(f"Ruta: {ruta['ruta']}")
        print(f"Trainer: {ruta['trainer']}")
        print(f"Salon: {ruta['salon']}")
        print(f"Horario: {ruta['horario']}")
        print(f"Fecha de Inicio: {ruta['fecha_inicio']}")
        print(f"Fecha de Fin: {ruta['fecha_fin']}")

        if "campers" in ruta and ruta["campers"]:
            print("\nCampers Asignados:")
            for id_camper in ruta["campers"]:
                print(id_camper)
        else:
            print("No hay campers asignados a esta ruta")


def modificar_rutas():
    with open("object.json", "r") as f:
        campers_file = json.load(f)
    with open("rutasf.json", "r") as f:
        rutas_file = json.load(f)

    campers_aprobados = [
        camper["no_id"] for camper in campers_file if camper["estado"] == "Aprobado"
    ]

    id_estudiante = int(input("Ingrese el ID del estudiante a matricular: "))
    if id_estudiante in campers_aprobados:
        print("Rutas disponibles:")
        rutas_disponibles = ["RutaNodeJS", "RutaJava", "RutaNetCore"]
        for i, ruta in enumerate(rutas_disponibles, 1):
            print(f"{i}. {ruta}")

        opcion_ruta = int(
            input("Seleccione la ruta (Ingrese el número correspondiente): ")
        )

        ruta_seleccionada = rutas_disponibles[opcion_ruta - 1]
        print(f"Ha seleccionado la ruta: {ruta_seleccionada}")
        trainers_disponibles = set()
        rutas_filtradas = []
        for ruta in rutas_file.values():
            if ruta["ruta"] == ruta_seleccionada:
                trainers_disponibles.add(ruta["trainer"])
                rutas_filtradas.append(ruta)
        trainers_disponibles = list(trainers_disponibles)
        for i, trainer in enumerate(trainers_disponibles, 1):
            print(f"{i}. {trainer}")
        opcion_trainer = int(
            input("Seleccione el trainer (Ingrese el número correspondiente): ")
        )
        trainer_seleccionado = trainers_disponibles[opcion_trainer - 1]
        rutas_filtradas_por_trainer = []
        fecha_inicio_disponibles = set()
        for ruta in rutas_filtradas:
            if ruta["trainer"] == trainer_seleccionado:
                fecha_inicio_disponibles.add(ruta["fecha_inicio"])
                rutas_filtradas_por_trainer.append(ruta)

        fecha_inicio_disponibles = list(fecha_inicio_disponibles)
        for i, fecha in enumerate(fecha_inicio_disponibles, 1):
            print(f"{i}. {fecha}")
        opcion_fecha = int(input("Seleccione la fecha de inicio: "))
        fecha_seleccionada = fecha_inicio_disponibles[opcion_fecha - 1]
        rutas_filtradas_por_fecha = []
        salones_disponibles = set()
        for ruta in rutas_filtradas_por_trainer:
            if ruta["fecha_inicio"] == fecha_seleccionada:
                rutas_filtradas_por_fecha.append(ruta)
                salones_disponibles.add(ruta["salon"])

        salones_disponibles = list(salones_disponibles)
        for i, salon in enumerate(salones_disponibles, 1):
            print(f"{i}. {salon}")
        opcion_salon = int(input("Seleccione el salón."))
        salon_seleccionado = salones_disponibles[opcion_salon - 1]

        rutas_filtradas_por_salon = []
        horarios_disponibles = set()
        for ruta in rutas_filtradas_por_fecha:
            if ruta["salon"] == salon_seleccionado:
                rutas_filtradas_por_salon.append(ruta)
                horarios_disponibles.add(ruta["horario"])
        horarios_disponibles = list(horarios_disponibles)
        print(
            "\n Horario A: 6a.m.-10a.m. \n Horario B: 10a.m.-2p.m. \n Horario C: 2p.m.-6p.m. \n Horario D: 6p.m.-10p.m."
        )
        for i, horario in enumerate(horarios_disponibles, 1):
            print(f"{i}. {horario}")
        opcion_horario = int(input("Seleccione el horario."))
        horario_seleccionado = horarios_disponibles[opcion_horario - 1]

        ruta_final = None
        for ruta in rutas_filtradas_por_salon:
            if ruta["horario"] == horario_seleccionado:
                ruta_final = ruta
                break

        if len(ruta_final["campers"]) < 33:
            ruta_final["campers"].append(id_estudiante)
            print(
                f"El estudiante con ID {id_estudiante}, ha sido anadido a la ruta correctamente"
            )

            for estudiante in campers_file:
                if estudiante["no_id"] == id_estudiante:
                    id_ruta_actual = estudiante["id_ruta"]
                    # rutas_file[id_ruta_actual]["campers"].remove(id_estudiante)
                    estudiante["id_ruta"] = ruta_final["idruta"]
                    estudiante["trainer"] = ruta_final["trainer"]
                    estudiante["ruta"] = ruta_final["ruta"]
                    break

            rutas_file[id_ruta_actual]["campers"].remove(id_estudiante)
            # Actualizar rutas y campers JSONs
            with open("rutasf.json", "w") as f:
                json.dump(rutas_file, f, indent=2)
            with open("object.json", "w") as f:
                json.dump(campers_file, f, indent=2)
        else:
            print("La ruta seleccionada no tiene cupo disponible.")

    else:
        print("Estudiante no encontrado o no tiene estado 'Aprobado'.")


def calificaciones_modulos():
    with open("object.json", "r") as file:
        campers_data = json.load(file)

    campers_aprobados = [
        camper for camper in campers_data if camper["estado"] == "Aprobado"
    ]

    ids_aprobados = [camper["no_id"] for camper in campers_aprobados]

    if not ids_aprobados:
        print("No hay campers aprobados para asignar calificaciones.")
        return
    id_camper = int(
        input(
            "Digite el ID del camper para registrar las calificaciones de los módulos: "
        )
    )

    if id_camper not in ids_aprobados:
        print("El ID ingresado no corresponde a un camper aprobado.")
        return

    with open("rutasf.json", "r") as rutas_file:
        rutas_data = json.load(rutas_file)

    # REVISAR si el ID se encuentra en alguna ruta
    id_en_ruta = False
    for ruta_info in rutas_data.values():
        if id_camper in ruta_info["campers"]:
            id_en_ruta = True
            break

    if not id_en_ruta:
        print(
            "No se puede registrar calificaciones. Este estudiante aún no tiene ruta asignada."
        )
        return

    with open("notas_campers.json", "r") as file:  ######################
        notas_modulos = json.load(file)

    # REVISAR si ya se introdujeron calificaciones para el estudiante
    if str(id_camper) in notas_modulos:
        print("Ya se introdujeron calificaciones de este estudiante.")
        return

    calificaciones = {}
    riesgo = False

    for i in range(1, 6):  # 5 SON 5 MODULOS
        resultado_teoria = float(
            input(f"Digite resultado prueba teórica para el módulo {i}: ")
        )
        resultado_practica = float(
            input(f"Digite resultado prueba práctica para el módulo {i}: ")
        )
        resultado_talleres = float(
            input(f"Digite resultado talleres para el módulo {i}: ")
        )

        # Calcular el promedio ponderado
        calificacion_final = (
            (resultado_teoria * 0.3)
            + (resultado_practica * 0.6)
            + (resultado_talleres * 0.1)
        )

        if calificacion_final < 60:
            riesgo = True

        calificaciones[f"mod_{i}"] = calificacion_final

    calificaciones["riesgo"] = riesgo
    notas_modulos[str(id_camper)] = calificaciones

    with open("notas_campers.json", "w") as file:
        json.dump(notas_modulos, file, indent=2)
    print("Calificaciones guardadas exitosamente.")


# ----FUNCIONES PARA SECCION DE REPORTES-------


def campers_inscritos():
    with open("object.json", "r") as file:
        users = json.load(file)
        print("CAMPERS INSCRITOS: \n")
    for user in users:
        if user["estado"] == "Inscrito":
            print(
                "ID:",
                user["no_id"],
                "Nombre:",
                user["nombre"],
                "apellidos:",
                user["apellidos"],
            )
    file.close()


def campers_aprobados():
    with open("object.json", "r") as file:
        users = json.load(file)
        print("CAMPERS APROBADOS: \n")
    for user in users:
        if user["estado"] == "Aprobado":
            print(
                "ID:",
                user["no_id"],
                "Nombre:",
                user["nombre"],
                "apellidos:",
                user["apellidos"],
            )
    file.close()


def listar_trainers():
    with open("rutasf.json", "r") as f:
        rutas_file = json.load(f)
    trainers = set()
    for ruta_id, ruta_info in rutas_file.items():
        trainer = ruta_info["trainer"]
        trainers.add(trainer)
    print("ENTRENADORES: \n")
    for x, trainer in enumerate(trainers, 1):
        print(f"{x}. {trainer}")


def listar_rutas():
    with open("rutasf.json", "r") as f:
        rutas_file = json.load(f)

    rutas_nodejs = []
    rutas_java = []
    rutas_netcore = []

    campers_nodejs = set()
    trainers_nodejs = set()

    campers_java = set()
    trainers_java = set()

    campers_netcore = set()
    trainers_netcore = set()

    for key, ruta in rutas_file.items():
        if ruta["ruta"] == "RutaNodeJS":
            rutas_nodejs.append((key, ruta))
            campers_nodejs.update(set(ruta["campers"]))
            trainers_nodejs.add(ruta["trainer"])
        elif ruta["ruta"] == "RutaJava":
            rutas_java.append((key, ruta))
            campers_java.update(set(ruta["campers"]))
            trainers_java.add(ruta["trainer"])
        elif ruta["ruta"] == "RutaNetCore":
            rutas_netcore.append((key, ruta))
            campers_netcore.update(set(ruta["campers"]))
            trainers_netcore.add(ruta["trainer"])

    print("\n ----RUTA NODEJS----")
    if campers_nodejs:
        print("\nID de campers asignados: \n")
        for id_camper in campers_nodejs:
            print(id_camper)
    else:
        print("Aun no hay campers asignados para esta ruta.")
    print("\nTrainers Asignados:")
    for trainer in trainers_nodejs:
        print(trainer)

    print("\n----RUTA JAVA----")
    if campers_java:
        print("\nID de campers asignados: \n")
        for id_camper in campers_java:
            print(id_camper)
    else:
        print("Aun no hay campers asignados para esta ruta.")
    print("\nTrainers Asignados:")
    for trainer in trainers_java:
        print(trainer)

    print("\n----RUTA NETCORE----")
    if campers_netcore:
        print("\nID de campers asignados: \n")
        for id_camper in campers_netcore:
            print(id_camper)
    else:
        print("Aun no hay campers asignados para esta ruta.")
    print("\nTrainers Asignados:")
    for trainer in trainers_netcore:
        print(trainer)


def estudiantes_riesgo():
    with open("notas_campers.json", "r") as file_notas, open(
        "object.json", "r"
    ) as file_object:
        notas_modulos = json.load(file_notas)
        campers_info = json.load(file_object)

    campers_riesgo = [
        id_camper
        for id_camper, info in notas_modulos.items()
        if info.get("riesgo", True)
    ]

    if not campers_riesgo:
        print("No hay campers en riesgo.")
        return

    print("CAMPERS EN RIESGO: ")
    for i, id_camper in enumerate(campers_riesgo, start=1):
        info_camper = next(
            (camper for camper in campers_info if camper["no_id"] == int(id_camper)),
            None,
        )
        if info_camper:
            nombre_apellidos = f"{info_camper['nombre']} {info_camper['apellidos']}"
            print(f"{i}. ID: {id_camper}, Nombre: {nombre_apellidos}")


def resultados_modulos():
    with open("notas_campers.json", "r") as file_notas, open(
        "object.json", "r"
    ) as file_object:
        notas_modulos = json.load(file_notas)
        campers_info = json.load(file_object)

    for i in range(1, 6):
        modulo_key = f"mod_{i}"
        aprobados = [
            id_camper
            for id_camper in sorted(
                [
                    id_camper
                    for id_camper, info in notas_modulos.items()
                    if info.get(modulo_key, 0) > 60
                ]
            )
        ]
        reprobados = [
            id_camper
            for id_camper in sorted(
                [
                    id_camper
                    for id_camper, info in notas_modulos.items()
                    if info.get(modulo_key, 0) <= 60
                ]
            )
        ]

        print(f"\n ---MÓDULO {i}---")
        if aprobados:
            print("Aprobados:")
            for x, id_camper in enumerate(aprobados, 1):
                camper = next(
                    (c for c in campers_info if c["no_id"] == int(id_camper)), None
                )
                if camper:
                    print(
                        f"{x}. ID: {id_camper}, NOMBRE: {camper['nombre']}, RUTA: {camper['ruta']}, TRAINER: {camper['trainer']}"
                    )
        else:
            print("\n No hay estudiantes aprobados en esta sección.")

        if reprobados:
            print("\nReprobados:")
            for x, id_camper in enumerate(reprobados, 1):
                camper = next(
                    (c for c in campers_info if c["no_id"] == int(id_camper)), None
                )
                if camper:
                    print(
                        f"{x}. ID: {id_camper}, NOMBRE: {camper['nombre']}, RUTA: {camper['ruta']}, TRAINER: {camper['trainer']}"
                    )
        else:
            print("\n No hay estudiantes reprobados en esta sección.")


# --------------MENUS----------------------

opcion = None
print("------Bienvenido a la plataforma CAMPUS------")
while opcion != 4:
    opcion = input(
        "\n MENÚ PRINCIPAL \n 1. Campers. \n 2. Gestión de matriculas. \n 3. Reportes \n 4. SALIR \n"
    )
    if opcion == "1":
        opcion1 = None
        while opcion1 != "5":
            opcion1 = input(
                "\n ---CAMPERS--- \n 1. Registrar nuevo estudiante. \n 2. Visualizar estudiantes registrados. \n 3. Registrar resultado prueba de ingreso. \n 4. Registrar calificaciones módulos de entrenamiento. \n 5. SALIR. \n"
            )
            if opcion1 == "1":
                registrar_camper()
            elif opcion1 == "2":
                visualizar_camper()
            elif opcion1 == "3":
                registrar_prueba()
            elif opcion1 == "4":
                calificaciones_modulos()
            elif opcion1 == "5":
                break
            else:
                print(
                    "\n Opción inválida. Digite una opción válida de acuerdo al menú.\n"
                )

    elif opcion == "2":
        opcion2 = None
        while opcion2 != 4:
            opcion2 = input(
                "\n ---GESTION DE MATRICULA--- \n 1. Asignar automáticamente rutas para campers. \n 2. Modificar ruta para un camper especifico. \n 3. Visualizar matriculas. \n 4. SALIR \n"
            )
            if opcion2 == "1":
                asignar_rutas()
            elif opcion2 == "2":
                modificar_rutas()
            elif opcion2 == "3":
                visualizar_matricula()
            elif opcion2 == "4":
                break
            else:
                print(
                    "\n Opción inválida. Digite una opción válida de acuerdo al menú.\n"
                )

    elif opcion == "3":
        opcion3 = None
        while opcion3 != 7:
            opcion3 = input(
                "\n ---REPORTES--- \n 1. Listar campers incritos. \n 2. Listar campers que aprobaron examen inicial. \n 3. Listar entrenadores. \n 4. Listar estudiantes con bajo rendimiento. \n 5. Listar campers y trainer asociados a una ruta de entrenamiento. \n 6. Listar campers aprobados y reprobados por módulos. \n 7. SALIR. \n "
            )
            if opcion3 == "1":
                campers_inscritos()
            elif opcion3 == "2":
                campers_aprobados()
            elif opcion3 == "3":
                listar_trainers()
            elif opcion3 == "4":
                estudiantes_riesgo()
            elif opcion3 == "5":
                listar_rutas()
            elif opcion3 == "6":
                resultados_modulos()
            elif opcion3 == "7":
                break
            else:
                print(
                    "\n Opción inválida. Digite una opción válida de acuerdo al menú.\n"
                )
    elif opcion == "4":
        break
    else:
        print("\n Opción inválida. Digite una opción válida de acuerdo al menú.\n")
