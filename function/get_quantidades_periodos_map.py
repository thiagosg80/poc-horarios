from professor.model.aula import Aula


def get_quantidades_periodos_map(aulas: list[Aula]) -> dict:
    return {aula.turma: {'quantidade_maxima_periodos_consecutivos': aula.quantidade_maxima_periodos_consecutivos,
                         'quantidade_minima_periodos_consecutivos': aula.quantidade_minima_periodos_consecutivos}
            for aula in aulas}