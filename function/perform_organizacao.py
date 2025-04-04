from flask import Response
from OrganizadorHorarios import OrganizadorHorarios
from turma.function.grade.get_grade_file import get_grade_file


def perform_organizacao() -> Response:
    organizador = OrganizadorHorarios()
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    periodos = 5
    organizador.definir_horarios(dias, periodos)

    professores = [
        (1, 'andreia p', {'Segunda': 5, 'Quarta': 5, 'Sexta': 5}),
        (2, 'josiane', {'Terça': 2, 'Quarta': 2, 'Quinta': 1}),
        (3, 'maristela', {'Terça': 3, 'Quarta': 5}),
        (4, 'edson', {'Terça': 4, 'Quinta': 4}),
        (5, 'cristian', {'Segunda': 4, 'Quarta': 4}),
        (6, 'jeferson', {'Segunda': 3, 'Quinta': 5}),
        (7, 'robson', {'Segunda': 4, 'Quarta': 1, 'Sexta': 3}),
        (8, 'crissiane', {'Terça': 3, 'Sexta': 5})
    ]

    for id_prof, nome, disponibilidade in professores:
        organizador.adicionar_professor(id_prof, nome, disponibilidade)

    disciplinas = [
        (1, "Matemática"),
        (2, "Português"),
        (3, "Ciências"),
        (4, "História"),
        (5, "Geografia"),
        (6, "Inglês"),
        (7, "Educação Física"),
        (8, 'Iniciação Científica')
    ]

    for id_disc, nome in disciplinas:
        organizador.adicionar_disciplina(id_disc, nome)

    turmas = [
        (1, '161',
         {1: 5, 2: 5, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2},
         {1: 2, 2: 1, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}
        ),
        (2, '171',
         {2: 5, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2},
         {2: 1, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}
         )
    ]

    for id_turma, nome, disc_carga, prof_disc in turmas:
        organizador.adicionar_turma(id_turma, nome, disc_carga, prof_disc)

    organizador.gerar_horarios()

    nome_arquivo = "horarios_escolares.html"
    organizador.exportar_para_html(nome_arquivo)

    return get_grade_file({})