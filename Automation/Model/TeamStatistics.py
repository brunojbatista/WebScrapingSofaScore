from Automation.Model.BaseModel import BaseModel

class TeamStatistics(BaseModel):
    def __init__(self, ):
        super().__init__(
            id=None,
            time=None, # ft = full time | ht = half time | 2t = second time

            # ---------------------------------------------
            # Visão Geral da Partida
            ball_possession=None,
            expected_goals=None,
            big_chances=None,
            goalkeeper_saves=None,
            corners=None,
            faults=None,
            passes=None,
            disarms=None,
            fouls_direct_shots=None, # Faltas (Tiros Diretos)
            yellow_cards=None,

            # ---------------------------------------------
            # Informações de finalizações
            shots=None,
            shots_on_target=None,
            shots_hit_woodwork= None, # Chutes na trave
            shots_off_target=None,
            shots_saved=None,
            shots_inside_box=None, # Chutes dentro da área
            shots_outside_box=None, # Chutes fora da área

            # ---------------------------------------------
            # Informações de Ataque
            big_chances_scored=None,
            big_chances_missed=None,
            through_pass=None, # Passe em profundidade
            actions_penalty_area= None, # Ações com a bola na área de pênalti
            fouls_drawn_final_third=None, # Faltas sofridas no terço final
            offsides=None, # Impedimentos

            # ---------------------------------------------
            # Informações de Passes
            accurate_passes=None, # Passes certos
            throw_ins=None, # Leterais
            runs_final_third=None, # Entradas no terço final

            # ---------------------------------------------
            # Informações de Duelos
            tackles_lost=None, # Desarmes sofridos

            # ---------------------------------------------
            # Informações de Defesa
            total_tackles=None, # Total de desarme
            interceptions=None, 
            ball_recoveries=None,
            clearances=None, # Desarme de jogadas perigosas
        )