from Automation.Model.BaseModel import BaseModel

class TimeStatistics(BaseModel):
    def __init__(self, 
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
    ):
        super().__init__(
            id=id,
            time=time,
            # team=None, # home | away

            # ---------------------------------------------
            # Visão Geral da Partida
            ball_possession=ball_possession,
            expected_goals=expected_goals,
            big_chances=big_chances,
            goalkeeper_saves=goalkeeper_saves,
            corners=corners,
            faults=faults,
            passes=passes,
            disarms=disarms,
            fouls_direct_shots=fouls_direct_shots, # Faltas (Tiros Diretos)
            yellow_cards=yellow_cards,

            # ---------------------------------------------
            # Informações de finalizações
            shots=shots,
            shots_on_target=shots_on_target,
            shots_hit_woodwork=shots_hit_woodwork, # Chutes na trave
            shots_off_target=shots_off_target,
            shots_saved=shots_saved,
            shots_inside_box=shots_inside_box, # Chutes dentro da área
            shots_outside_box=shots_outside_box, # Chutes fora da área

            # ---------------------------------------------
            # Informações de Ataque
            big_chances_scored=big_chances_scored,
            big_chances_missed=big_chances_missed,
            through_pass=through_pass, # Passe em profundidade
            actions_penalty_area=actions_penalty_area, # Ações com a bola na área de pênalti
            fouls_drawn_final_third=fouls_drawn_final_third, # Faltas sofridas no terço final
            offsides=offsides, # Impedimentos

            # ---------------------------------------------
            # Informações de Passes
            accurate_passes=accurate_passes, # Passes certos
            throw_ins=throw_ins, # Leterais
            runs_final_third=runs_final_third, # Entradas no terço final

            # ---------------------------------------------
            # Informações de Duelos
            tackles_lost=tackles_lost, # Desarmes sofridos

            # ---------------------------------------------
            # Informações de Defesa
            total_tackles=total_tackles, # Total de desarme
            interceptions=interceptions, 
            ball_recoveries=ball_recoveries,
            clearances=clearances, # Desarme de jogadas perigosas
        )
    
    def __eq__(self, other):
        if not isinstance(other, TimeStatistics): return False
        return (
            self.id == other.id and
            self.time == other.time and

            # ---------------------------------------------
            # Visão Geral da Partida
            self.ball_possession == other.ball_possession and
            self.expected_goals == other.expected_goals and
            self.big_chances == other.big_chances and
            self.goalkeeper_saves == other.goalkeeper_saves and
            self.corners == other.corners and
            self.faults == other.faults and
            self.passes == other.passes and
            self.disarms == other.disarms and
            self.fouls_direct_shots == other.fouls_direct_shots and # Faltas (Tiros Diretos)
            self.yellow_cards == other.yellow_cards and

            # ---------------------------------------------
            # Informações de finalizações
            self.shots == other.shots and
            self.shots_on_target == other.shots_on_target and
            self.shots_hit_woodwork == other.shots_hit_woodwork and # Chutes na trave
            self.shots_off_target == other.shots_off_target and
            self.shots_saved == other.shots_saved and
            self.shots_inside_box == other.shots_inside_box and # Chutes dentro da área
            self.shots_outside_box == other.shots_outside_box and # Chutes fora da área

            # ---------------------------------------------
            # Informações de Ataque
            self.big_chances_scored == other.big_chances_scored and
            self.big_chances_missed == other.big_chances_missed and
            self.through_pass == other.through_pass and # Passe em profundidade
            self.actions_penalty_area == other.actions_penalty_area and # Ações com a bola na área de pênalti
            self.fouls_drawn_final_third == other.fouls_drawn_final_third and # Faltas sofridas no terço final
            self.offsides == other.offsides and # Impedimentos

            # ---------------------------------------------
            # Informações de Passes
            self.accurate_passes == other.accurate_passes and # Passes certos
            self.throw_ins == other.throw_ins and # Leterais
            self.runs_final_third == other.runs_final_third and # Entradas no terço final

            # ---------------------------------------------
            # Informações de Duelos
            self.tackles_lost == other.tackles_lost and # Desarmes sofridos

            # ---------------------------------------------
            # Informações de Defesa
            self.total_tackles == other.total_tackles and # Total de desarme
            self.interceptions == other.interceptions and 
            self.ball_recoveries == other.ball_recoveries and
            self.clearances == other.clearances # Desarme de jogadas perigosas
        )