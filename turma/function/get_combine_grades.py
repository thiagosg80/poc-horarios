from turma.function.get_cell import get_cell
import copy
import random
from typing import List

from ortools.sat.python import cp_model

from function.get_dias_da_semana import get_dias_da_semana
from model.cell import Cell
from turma.function.get_periodos_ordens import get_periodos_ordens


def get_combined_grades(grades_by_professor: List[dict], turnos_as_string: set, turmas_map: dict) -> dict:
    """
    Uses a CP-SAT model to find a valid combination of individual professor schedules.
    Includes a retry-with-new-sample mechanism for performance and robustness.
    """
    dias_da_semana: List[str] = get_dias_da_semana()
    periodos_ordens: List[int] = get_periodos_ordens()
    combined_grades_result: dict = {}

    for turno in turnos_as_string:
        print(f"--- Iniciando combinação para o turno: {turno} ---")

        # 1. Coletar grades e professores originais para este turno
        original_professors_in_turno = []
        for grade_professor in grades_by_professor:
            if turno in grade_professor['grades'] and grade_professor['grades'][turno]:
                original_professors_in_turno.append({
                    'professor_nome': grade_professor['professor_nome'],
                    'grades': grade_professor['grades'][turno]
                })

        if not original_professors_in_turno:
            continue

        # --- Início da Lógica de Múltiplas Tentativas ---
        MAX_ATTEMPTS = 5
        MAX_GRADES_PER_PROFESSOR = 1000
        solution_found = False
        status = None
        solver = None
        choices = {}
        professors_for_solution = None

        for attempt in range(MAX_ATTEMPTS):
            print(f"Turno {turno}: Tentativa de combinação {attempt + 1}/{MAX_ATTEMPTS}...")
            
            # 2. Amostragem das grades para a tentativa atual
            professors_in_attempt = copy.deepcopy(original_professors_in_turno)
            random.seed(42 + attempt)  # Seed diferente para cada tentativa
            for prof_data in professors_in_attempt:
                num_grades = len(prof_data['grades'])
                if num_grades > MAX_GRADES_PER_PROFESSOR:
                    if attempt == 0: # Imprimir aviso apenas na primeira tentativa
                         print(f"AVISO: Professor {prof_data['professor_nome']} tem {num_grades} grades. "
                               f"Usando uma amostra de {MAX_GRADES_PER_PROFESSOR} para otimizar a performance.")
                    prof_data['grades'] = random.sample(prof_data['grades'], MAX_GRADES_PER_PROFESSOR)

            # 3. Criar o modelo e as variáveis para a tentativa atual
            model = cp_model.CpModel()
            choices = {}
            for i, prof_data in enumerate(professors_in_attempt):
                for j in range(len(prof_data['grades'])):
                    choices[(i, j)] = model.NewBoolVar(f"choice_{i}_{j}")

            # 4. Adicionar Restrições
            # R1: Exatamente uma grade por professor
            for i, prof_data in enumerate(professors_in_attempt):
                model.AddExactlyOne([choices[(i, j)] for j in range(len(prof_data['grades']))])

            # R2: Sem conflitos de slot
            turmas_by_turno = __get_turmas_by_turno(turno, turmas_map)
            for dia in dias_da_semana:
                for turma_id in turmas_by_turno:
                    for per_ordem in periodos_ordens:
                        slot_allocators = []
                        for i, prof_data in enumerate(professors_in_attempt):
                            for j, grade in enumerate(prof_data['grades']):
                                cell = __get_cell(grade, dia, turma_id, per_ordem)
                                if isinstance(cell, dict) and cell['allocated'] or isinstance(cell, Cell) and cell.allocation:
                                    slot_allocators.append(choices[(i, j)])
                        if len(slot_allocators) > 1:
                            model.AddAtMostOne(slot_allocators)
            
            # 5. Resolver o modelo
            solver = cp_model.CpSolver()
            status = solver.Solve(model)

            # 6. Verificar se a solução foi encontrada
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                print(f"Solução de combinação encontrada na tentativa {attempt + 1} para o turno {turno}.")
                solution_found = True
                professors_for_solution = professors_in_attempt # Salvar os dados usados nesta tentativa
                break # Sair do loop de tentativas
        # --- Fim da Lógica de Múltiplas Tentativas ---

        # 7. Processar a solução (se encontrada)
        if solution_found:
            chosen_grades = []
            for i, prof_data in enumerate(professors_for_solution):
                for j, grade in enumerate(prof_data['grades']):
                    if solver.Value(choices[(i, j)]) == 1:
                        chosen_grades.append(grade)
                        break
            
            final_combined_grade = {}
            turmas_by_turno = __get_turmas_by_turno(turno, turmas_map)
            for dia in dias_da_semana:
                final_combined_grade[dia] = {}
                for turma_id in turmas_by_turno:
                    final_combined_grade[dia][turma_id] = {'cells': []}
                    for per_ordem in periodos_ordens:
                        final_cell = get_cell(dia, turma_id, per_ordem)
                        for grade in chosen_grades:
                            cell = __get_cell(grade, dia, turma_id, per_ordem)
                            if isinstance(cell, dict) and cell['allocated'] or isinstance(cell, Cell) and cell.allocation:
                                final_cell = cell
                                break
                        final_combined_grade[dia][turma_id]['cells'].append(final_cell)
            
            combined_grades_result[turno] = [final_combined_grade]
        else:
            print(f"Nenhuma combinação de grades foi encontrada para o turno {turno} após {MAX_ATTEMPTS} tentativas. "
                  f"Status final: {solver.StatusName(status) if solver else 'N/A'}")
            combined_grades_result[turno] = []

    return combined_grades_result



def __get_turmas_by_turno(turno, turmas_map) -> List[str]:
    return list([x for x in turmas_map if turmas_map.get(x).turno == turno])




def __get_cell(container, dia_da_semana, turma_by_turno, periodo_ordem) -> dict:
    if dia_da_semana in container:
        dia = container[dia_da_semana]
        if turma_by_turno in dia:
            return list([x for x in dia[turma_by_turno].cells if x.position == periodo_ordem])[0]

    return get_cell(dia_da_semana, turma_by_turno, periodo_ordem)