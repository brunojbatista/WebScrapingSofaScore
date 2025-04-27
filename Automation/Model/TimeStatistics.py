from Automation.Model.BaseModel import BaseModel

class TimeStatistics(BaseModel):
    def __init__(self, ):
        super().__init__(
            id=None,
            time=None, # ft = full time | ht = half time | 2t = second time
            # team=None, # home | away

            # ---------------------------------------------
            # Visão Geral da Partida
            ball_possession={"home_value": None, "away_value": None},
            expected_goals={"home_value": None, "away_value": None},
            big_chances={"home_value": None, "away_value": None},
            goalkeeper_saves={"home_value": None, "away_value": None},
            corners={"home_value": None, "away_value": None},
            faults={"home_value": None, "away_value": None},
            passes={"home_value": None, "away_value": None},
            disarms={"home_value": None, "away_value": None},
            fouls_direct_shots={"home_value": None, "away_value": None}, # Faltas (Tiros Diretos)
            yellow_cards={"home_value": None, "away_value": None},

            # ---------------------------------------------
            # Informações de finalizações
            shots={"home_value": None, "away_value": None},
            shots_on_target={"home_value": None, "away_value": None},
            shots_hit_woodwork= {"home_value": None, "away_value": None}, # Chutes na trave
            shots_off_target={"home_value": None, "away_value": None},
            shots_saved={"home_value": None, "away_value": None},
            shots_inside_box={"home_value": None, "away_value": None}, # Chutes dentro da área
            shots_outside_box={"home_value": None, "away_value": None}, # Chutes fora da área

            # ---------------------------------------------
            # Informações de Ataque
            big_chances_scored={"home_value": None, "away_value": None},
            big_chances_missed={"home_value": None, "away_value": None},
            through_pass={"home_value": None, "away_value": None}, # Passe em profundidade
            actions_penalty_area= {"home_value": None, "away_value": None}, # Ações com a bola na área de pênalti
            fouls_drawn_final_third={"home_value": None, "away_value": None}, # Faltas sofridas no terço final
            offsides={"home_value": None, "away_value": None}, # Impedimentos

            # ---------------------------------------------
            # Informações de Passes
            accurate_passes={"home_value": None, "away_value": None}, # Passes certos
            throw_ins={"home_value": None, "away_value": None}, # Leterais
            runs_final_third={"home_value": None, "away_value": None}, # Entradas no terço final

            # ---------------------------------------------
            # Informações de Duelos
            tackles_lost={"home_value": None, "away_value": None}, # Desarmes sofridos

            # ---------------------------------------------
            # Informações de Defesa
            total_tackles={"home_value": None, "away_value": None}, # Total de desarme
            interceptions={"home_value": None, "away_value": None}, 
            ball_recoveries={"home_value": None, "away_value": None},
            clearances={"home_value": None, "away_value": None}, # Desarme de jogadas perigosas
        )