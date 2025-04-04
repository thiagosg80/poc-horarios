import random
from collections import defaultdict


class OrganizadorHorarios:
    def __init__(self):
        self.professores = {}
        self.disciplinas = {}
        self.turmas = {}
        self.horarios_disponiveis = []
        self.grade_horaria = defaultdict(dict)
        self.ordem_dias = []
        self.problemas_alocacao = []  # Lista para armazenar problemas encontrados

    def adicionar_professor(self, id_professor, nome, disponibilidade=None):
        """
        Adiciona um professor ao sistema com sua disponibilidade específica.

        Args:
            disponibilidade: Lista de tuplas (dia, periodo) ou dicionário {dia: numero_de_periodos}
        """
        if disponibilidade is None:
            # Se nenhuma disponibilidade for especificada, considera disponível em todos os horários
            disponibilidade = self.horarios_disponiveis.copy()
        elif isinstance(disponibilidade, dict):
            # Se for dicionário no formato {dia: numero_de_periodos}
            disponibilidade_final = []
            for dia, num_periodos in disponibilidade.items():
                # Para cada dia, adiciona os períodos disponíveis (do 1 até o número especificado)
                for periodo in range(1, num_periodos + 1):
                    disponibilidade_final.append((dia, periodo))
            disponibilidade = disponibilidade_final

        self.professores[id_professor] = {
            'nome': nome,
            'disponibilidade': disponibilidade
        }

    def adicionar_disciplina(self, id_disciplina, nome):
        self.disciplinas[id_disciplina] = {
            'nome': nome
        }

    def adicionar_turma(self, id_turma, nome, disciplinas_carga, professores_disciplinas):
        """
        Adiciona uma turma ao sistema.

        Args:
            id_turma: Identificador da turma
            nome: Nome da turma
            disciplinas_carga: Dicionário com {id_disciplina: carga_horaria}
            professores_disciplinas: Dicionário com {id_disciplina: id_professor}
        """
        self.turmas[id_turma] = {
            'nome': nome,
            'disciplinas': disciplinas_carga,
            'professores_disciplinas': professores_disciplinas
        }

    def definir_horarios(self, dias_semana, periodos_por_dia):
        """Define a grade de horários disponíveis."""
        self.horarios_disponiveis = []
        self.ordem_dias = dias_semana  # Armazenar a ordem original dos dias
        for dia in dias_semana:
            for periodo in range(1, periodos_por_dia + 1):
                self.horarios_disponiveis.append((dia, periodo))

    def verificar_disponibilidade(self, id_professor, dia, periodo):
        """Verifica se um professor está disponível em determinado horário."""
        return (dia, periodo) in self.professores[id_professor]['disponibilidade']

    def _encontrar_professor_para_disciplina(self, id_turma, id_disciplina, dia, periodo):
        """Encontra um professor disponível para lecionar a disciplina na turma."""
        # Obter o professor associado à disciplina para esta turma
        id_professor = self.turmas[id_turma]['professores_disciplinas'].get(id_disciplina)

        # Verificar se o professor existe e está disponível
        if id_professor and self.verificar_disponibilidade(id_professor, dia, periodo):
            return id_professor

        return None

    def _atualizar_disponibilidade(self, id_professor, dia, periodo):
        """Remove o horário da disponibilidade do professor."""
        if (dia, periodo) in self.professores[id_professor]['disponibilidade']:
            self.professores[id_professor]['disponibilidade'].remove((dia, periodo))

    def _encontrar_slots_consecutivos(self, id_turma, dia, qtd_slots, id_disciplina):
        """
        Encontra slots consecutivos disponíveis em um determinado dia para
        alocação de múltiplas aulas da mesma disciplina.
        """
        periodos_dia = [p for d, p in self.horarios_disponiveis if d == dia]
        periodos_dia.sort()

        for inicio in periodos_dia:
            slots_consecutivos = []

            # Verifica se temos slots consecutivos suficientes
            for periodo in range(inicio, inicio + qtd_slots):
                # Verifica se o período existe e está disponível
                if periodo not in periodos_dia:
                    break

                # Verifica se o horário já está ocupado para esta turma
                if (dia, periodo) in self.grade_horaria[id_turma]:
                    break

                # Verifica se há professor disponível
                id_professor = self._encontrar_professor_para_disciplina(
                    id_turma, id_disciplina, dia, periodo
                )

                if not id_professor:
                    break

                slots_consecutivos.append((periodo, id_professor))

            # Se encontramos slots suficientes
            if len(slots_consecutivos) == qtd_slots:
                return slots_consecutivos

        return None

    def _distribuir_dois_periodos(self, id_turma, id_disciplina):
        """
        Tenta distribuir dois períodos de uma disciplina em dias diferentes.
        Se não for possível, aloca os dois períodos consecutivos no mesmo dia.

        Retorna:
            True se conseguiu alocar os dois períodos, False caso contrário
        """
        # Primeiro tenta alocar em dias diferentes
        dias_disponiveis = list(set(dia for dia, _ in self.horarios_disponiveis))
        random.shuffle(dias_disponiveis)

        # Lista para armazenar os dias onde conseguimos alocar uma aula
        dias_alocados = []
        periodos_alocados = []
        professores_alocados = []

        # Tenta alocar o primeiro período em qualquer dia disponível
        for dia in dias_disponiveis:
            horarios_do_dia = [(d, p) for d, p in self.horarios_disponiveis if d == dia]
            random.shuffle(horarios_do_dia)

            for d, periodo in horarios_do_dia:
                # Verifica se o horário já está ocupado para esta turma
                if (d, periodo) in self.grade_horaria[id_turma]:
                    continue

                # Encontra um professor para a disciplina
                id_professor = self._encontrar_professor_para_disciplina(
                    id_turma, id_disciplina, d, periodo
                )

                if id_professor:
                    dias_alocados.append(d)
                    periodos_alocados.append(periodo)
                    professores_alocados.append(id_professor)
                    break

            if dias_alocados:
                break

        # Se conseguiu alocar o primeiro período, tenta alocar o segundo em outro dia
        if dias_alocados:
            # Filtra dias diferentes do primeiro alocado
            outros_dias = [dia for dia in dias_disponiveis if dia != dias_alocados[0]]
            random.shuffle(outros_dias)

            for dia in outros_dias:
                horarios_do_dia = [(d, p) for d, p in self.horarios_disponiveis if d == dia]
                random.shuffle(horarios_do_dia)

                for d, periodo in horarios_do_dia:
                    # Verifica se o horário já está ocupado para esta turma
                    if (d, periodo) in self.grade_horaria[id_turma]:
                        continue

                    # Encontra um professor para a disciplina (preferencialmente o mesmo)
                    id_professor = self._encontrar_professor_para_disciplina(
                        id_turma, id_disciplina, d, periodo
                    )

                    # Tenta usar o mesmo professor se possível
                    if id_professor and id_professor == professores_alocados[0]:
                        dias_alocados.append(d)
                        periodos_alocados.append(periodo)
                        professores_alocados.append(id_professor)
                        break
                    elif id_professor and not id_professor == professores_alocados[0]:
                        # Se não for o mesmo professor, guarda como opção alternativa
                        dias_alocados.append(d)
                        periodos_alocados.append(periodo)
                        professores_alocados.append(id_professor)
                        break

                if len(dias_alocados) == 2:
                    break

        # Se não conseguiu alocar em dois dias diferentes, tenta alocar consecutivamente
        if len(dias_alocados) < 2:
            # Limpa os dados se só conseguiu alocar parcialmente
            if dias_alocados:
                dias_alocados = []
                periodos_alocados = []
                professores_alocados = []

            # Tenta alocar consecutivamente em um único dia
            for dia in dias_disponiveis:
                slots = self._encontrar_slots_consecutivos(id_turma, dia, 2, id_disciplina)

                if slots:
                    # Se encontrou slots consecutivos, aloca os dois períodos
                    for periodo, id_professor in slots:
                        dias_alocados.append(dia)
                        periodos_alocados.append(periodo)
                        professores_alocados.append(id_professor)
                    break

        # Se conseguiu alocar os dois períodos, registra na grade horária
        if len(dias_alocados) == 2:
            for i in range(2):
                self.grade_horaria[id_turma][(dias_alocados[i], periodos_alocados[i])] = {
                    'disciplina': id_disciplina,
                    'professor': professores_alocados[i]
                }
                self._atualizar_disponibilidade(professores_alocados[i], dias_alocados[i], periodos_alocados[i])
            return True

        return False

    def _analisar_problemas_alocacao(self, id_turma, id_disciplina, carga_horaria, aulas_alocadas):
        """
        Analisa os problemas de alocação para gerar sugestões.
        Retorna as possíveis causas e sugestões.
        """
        nome_disciplina = self.disciplinas[id_disciplina]['nome']
        nome_turma = self.turmas[id_turma]['nome']

        # Verificar se a disciplina tem professor associado
        id_professor = self.turmas[id_turma]['professores_disciplinas'].get(id_disciplina)

        if not id_professor:
            return {
                "tipo": "sem_professor",
                "disciplina": nome_disciplina,
                "turma": nome_turma,
                "aulas_pendentes": carga_horaria - aulas_alocadas,
                "sugestoes": ["Adicionar um professor que possa lecionar esta disciplina."]
            }

        # Verificar disponibilidade do professor
        disponibilidade = len(self.professores[id_professor]['disponibilidade'])
        professor_nome = self.professores[id_professor]['nome']

        sugestoes = []

        # Se não há disponibilidade suficiente para alocar as aulas pendentes
        if disponibilidade < (carga_horaria - aulas_alocadas):
            sugestoes.append(f"Aumentar a disponibilidade do(a) professor(a) {professor_nome}.")
            sugestoes.append(f"Atribuir outro professor à disciplina {nome_disciplina} para esta turma.")
        else:
            # Se há disponibilidade, mas em horários conflitantes
            sugestoes.append("Verificar conflitos de horário com outras turmas.")
            sugestoes.append(
                f"Distribuir melhor a disponibilidade do(a) professor(a) {professor_nome} ao longo da semana.")

            # Verificar se há sobreposição de disciplinas em uma turma
            disciplinas_alocadas = {}
            for (dia, periodo), aula in self.grade_horaria[id_turma].items():
                if aula['disciplina'] not in disciplinas_alocadas:
                    disciplinas_alocadas[aula['disciplina']] = 0
                disciplinas_alocadas[aula['disciplina']] += 1

            # Se a turma já tem muitas disciplinas alocadas
            if len(disciplinas_alocadas) > 0:
                sugestoes.append("Reorganizar a prioridade das disciplinas para esta turma.")

        return {
            "tipo": "disponibilidade_insuficiente",
            "disciplina": nome_disciplina,
            "turma": nome_turma,
            "aulas_pendentes": carga_horaria - aulas_alocadas,
            "professor": {
                "id": id_professor,
                "nome": professor_nome,
                "disponibilidade": disponibilidade
            },
            "sugestoes": sugestoes
        }

    def gerar_horarios(self):
        self.grade_horaria = defaultdict(dict)
        self.problemas_alocacao = []

        # Cria cópias das listas de disponibilidade
        for id_professor in self.professores:
            self.professores[id_professor]['disponibilidade'] = list(self.professores[id_professor]['disponibilidade'])

        # Calcular disponibilidade total de cada professor para priorização
        disponibilidade_total = {}
        for id_professor, dados in self.professores.items():
            disponibilidade_total[id_professor] = len(dados['disponibilidade'])

        # Para cada turma
        for id_turma, turma in self.turmas.items():
            # Mapeamento de professores por disciplina com sua disponibilidade
            professores_disciplinas = {}
            for id_disciplina, id_professor in turma['professores_disciplinas'].items():
                if id_professor in disponibilidade_total:
                    professores_disciplinas[id_disciplina] = (id_professor, disponibilidade_total[id_professor])

            # Ordenar disciplinas por:
            # 1. Disponibilidade limitada do professor (crescente)
            # 2. Carga horária (decrescente)
            disciplinas_ordenadas = []
            for id_disciplina, carga in turma['disciplinas'].items():
                if id_disciplina in professores_disciplinas:
                    prof_id, disp = professores_disciplinas[id_disciplina]
                    # Criar um score de prioridade: menor disponibilidade e maior carga = maior prioridade
                    prioridade = (disp, -carga)
                    disciplinas_ordenadas.append((id_disciplina, carga, prioridade))

            # Ordenar por prioridade
            disciplinas_ordenadas.sort(key=lambda x: x[2])

            # Agora processa disciplinas na ordem de prioridade
            for id_disciplina, carga_horaria, _ in disciplinas_ordenadas:
                aulas_alocadas = 0

                # Trata disciplinas com carga 2 - tenta distribuir em dias diferentes primeiro
                if carga_horaria == 2:
                    if self._distribuir_dois_periodos(id_turma, id_disciplina):
                        aulas_alocadas = 2
                    else:
                        problema = self._analisar_problemas_alocacao(id_turma, id_disciplina, carga_horaria,
                                                                     aulas_alocadas)
                        self.problemas_alocacao.append(problema)
                        continue

                # Trata outras cargas horárias
                while aulas_alocadas < carga_horaria:
                    # Contagem de aulas por dia para esta disciplina
                    aulas_por_dia = defaultdict(int)
                    for (dia, _), aula in self.grade_horaria[id_turma].items():
                        if aula['disciplina'] == id_disciplina:
                            aulas_por_dia[dia] += 1

                    # Ordena os dias por quantidade de aulas já alocadas (prioriza os com menos aulas)
                    dias_disponiveis = list(set(dia for dia, _ in self.horarios_disponiveis))
                    dias_disponiveis.sort(key=lambda d: aulas_por_dia[d])

                    alocado = False

                    # Para disciplinas com mais de 2 aulas restantes, tenta alocar 2 consecutivas
                    if carga_horaria - aulas_alocadas >= 2:
                        for dia in dias_disponiveis:
                            # Não permitir mais de 2 aulas da mesma disciplina no mesmo dia
                            if aulas_por_dia[dia] >= 2:
                                continue

                            slots = self._encontrar_slots_consecutivos(id_turma, dia, 2, id_disciplina)

                            if slots:
                                for periodo, id_professor in slots:
                                    self.grade_horaria[id_turma][(dia, periodo)] = {
                                        'disciplina': id_disciplina,
                                        'professor': id_professor
                                    }
                                    self._atualizar_disponibilidade(id_professor, dia, periodo)
                                    aulas_por_dia[dia] += 1

                                aulas_alocadas += 2
                                alocado = True
                                break

                    # Se não conseguimos alocar em bloco ou tem apenas 1 aula para alocar
                    if not alocado and aulas_alocadas < carga_horaria:
                        # Ordena horários para tentar minimizar fragmentação
                        horarios_disponiveis = []
                        for dia in dias_disponiveis:
                            # Limita a 2 aulas por dia da mesma disciplina
                            if aulas_por_dia[dia] >= 2:
                                continue

                            # Busca todos os períodos disponíveis neste dia
                            for periodo in range(1, 6):  # Assumindo 5 períodos por dia
                                if (dia, periodo) not in self.grade_horaria[id_turma]:
                                    horarios_disponiveis.append((dia, periodo))

                        # Ordena para privilegiar períodos adjacentes às aulas já alocadas
                        horarios_disponiveis.sort(key=lambda x: aulas_por_dia[x[0]])

                        for dia, periodo in horarios_disponiveis:
                            # Encontra professor disponível
                            id_professor = self._encontrar_professor_para_disciplina(id_turma, id_disciplina, dia,
                                                                                     periodo)

                            if id_professor:
                                # Aloca a aula
                                self.grade_horaria[id_turma][(dia, periodo)] = {
                                    'disciplina': id_disciplina,
                                    'professor': id_professor
                                }
                                self._atualizar_disponibilidade(id_professor, dia, periodo)
                                aulas_alocadas += 1
                                aulas_por_dia[dia] += 1
                                alocado = True

                                if aulas_alocadas >= carga_horaria:
                                    break

                    if not alocado:
                        problema = self._analisar_problemas_alocacao(id_turma, id_disciplina, carga_horaria,
                                                                     aulas_alocadas)
                        self.problemas_alocacao.append(problema)
                        break

    def exportar_para_html(self, nome_arquivo="horarios_escolares.html"):
        html = """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Horários Escolares</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                h1, h2 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                    background-color: #fff;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                th, td {
                    padding: 12px 15px;
                    text-align: center;
                    border: 1px solid #ddd;
                    vertical-align: top;
                }
                th {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .periodo {
                    margin-bottom: 15px;
                    padding: 8px;
                    background-color: #e3f2fd;
                    border-radius: 4px;
                }
                .problemas {
                    margin-top: 40px;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                .problema {
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: #fff9c4;
                    border-left: 4px solid #ffc107;
                    border-radius: 4px;
                }
                .sugestoes {
                    margin-top: 10px;
                    padding-left: 20px;
                }
                .sugestoes li {
                    margin-bottom: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Horários Escolares</h1>
        """

        todos_dias = self.ordem_dias
        todas_turmas = sorted(self.turmas.keys())
        todos_periodos = sorted(
            set(periodo for horarios in self.grade_horaria.values() for _, periodo in horarios.keys()))

        html += """
            <table>
                <thead>
                    <tr>
                        <th>Dia</th>
        """

        for id_turma in todas_turmas:
            turma = self.turmas[id_turma]
            html += f"<th>{turma['nome']}</th>"

        html += """
                    </tr>
                </thead>
                <tbody>
        """

        for dia in todos_dias:
            html += f"<tr><td><strong>{dia}</strong></td>"

            for id_turma in todas_turmas:
                html += "<td>"

                for periodo in todos_periodos:
                    horarios = self.grade_horaria.get(id_turma, {})

                    html += f"<div class='periodo'>"
                    html += f"{periodo} - "

                    if (dia, periodo) in horarios:
                        aula = horarios[(dia, periodo)]
                        disciplina = self.disciplinas[aula['disciplina']]['nome']
                        professor = self.professores[aula['professor']]['nome']

                        html += f"""
                            {disciplina} - 
                            Prof. {professor}
                        """
                    else:
                        html += '---'

                    html += "</div>"

                html += "</td>"

            html += "</tr>"

        html += """
                </tbody>
            </table>
        """

        # Adicionar seção de problemas e sugestões se houver problemas
        if self.problemas_alocacao:
            html += """
            <div class="problemas">
                <h2>Problemas de Alocação e Sugestões</h2>
            """

            for problema in self.problemas_alocacao:
                html += f"""
                <div class="problema">
                    <p><strong>Problema:</strong> Não foi possível alocar {problema['aulas_pendentes']} aulas de {problema['disciplina']} para a turma {problema['turma']}.</p>
                """

                if problema['tipo'] == 'disponibilidade_insuficiente' and 'professor' in problema:
                    html += f"<p><strong>Professor:</strong> {problema['professor']['nome']} - {problema['professor']['disponibilidade']} horários disponíveis</p>"

                html += "<p><strong>Sugestões:</strong></p><ul class='sugestoes'>"
                for sugestao in problema['sugestoes']:
                    html += f"<li>{sugestao}</li>"
                html += "</ul></div>"

            html += "</div>"

        html += """
            </div>
        </body>
        </html>
        """

        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            file.write(html)

        print(f"Arquivo HTML gerado com sucesso: {nome_arquivo}")

    def exibir_sugestoes(self):
        """
        Exibe sugestões para resolver problemas de alocação.
        """
        if not self.problemas_alocacao:
            print("Não foram encontrados problemas na alocação das aulas.")
            return

        print("\n=== PROBLEMAS DE ALOCAÇÃO E SUGESTÕES ===")
        for i, problema in enumerate(self.problemas_alocacao, 1):
            print(f"\nProblema #{i}:")
            print(f"  Disciplina: {problema['disciplina']}")
            print(f"  Turma: {problema['turma']}")
            print(f"  Aulas pendentes: {problema['aulas_pendentes']}")

            if problema['tipo'] == 'sem_professor':
                print("  Diagnóstico: Não há professores disponíveis para esta disciplina.")
            elif problema['tipo'] == 'disponibilidade_insuficiente':
                print("  Diagnóstico: Disponibilidade insuficiente do professor.")
                if 'professor' in problema:
                    print(
                        f"    - {problema['professor']['nome']}: {problema['professor']['disponibilidade']} horários disponíveis")

            print("\n  Sugestões:")
            for j, sugestao in enumerate(problema['sugestoes'], 1):
                print(f"    {j}. {sugestao}")
            print()