import re
from typing import (
    List,
)

from Library_v1.Driver.DriverInterface import DriverInterface
from Automation.View.BaseView import BaseView
from Automation.Model.EventCell import EventCell
from Automation.Model.Match import Match
from Automation.Model.Time.TimeStatistics import TimeStatistics
from Automation.Model.Time.HalfTimeStatistics import HalfTimeStatistics
from Automation.Model.Time.SecondTimeStatistics import SecondTimeStatistics
from Automation.Model.Time.FullTimeStatistics import FullTimeStatistics
from Automation.Model.Competitions.Competition import Competition
from Library_v1.Utils.javascript import (
    JAVASCRIPT_CODE,
)
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    JavascriptException,
)
from Library_v1.Utils.time import (
    date_now,
    get_day_midnight,
    parse_date_with_format,
    format_date,
    parse_time,
    add_day,
)

SCRIPT_JS = JAVASCRIPT_CODE + r"""
    async function get_event_cells() {
        let event_cells = []
        const base_xpath = "//div[@data-panelid='date']/div/div[1]/div/div[last()]//a[@data-id]"
        if (!(await hasElements(base_xpath))) throw new Error("Não foi encontrado a lista de eventos")
        let elements = await getElements(base_xpath)
        for (let i = 0; i < elements.length; i++) {
            let el = elements[i]
            let id = await getAttr(el, 'data-id')
            let url = await getAttr(el, 'href')
            url = `https://www.sofascore.com${url}`
            let date_1 = await getText("./div/div/div/*[@data-testid='event_time']", el)
            let date_2 = await getText("./div/div/div/div[@data-testid='event_status']/span/*[name()='bdi']", el)
            let hometeam = await getText("./div/div/div//div[@data-testid='left_team']/*[last()]", el)
            let awayteam = await getText("./div/div/div//div[@data-testid='right_team']/*[last()]", el)

            let home_ft = null
            if (await hasElement("./div/div/div//div[@data-testid='left_score']/span[contains(@class, 'currentScore')]", el, 0))
                home_ft = await getText("./div/div/div//div[@data-testid='left_score']/span[contains(@class, 'currentScore')]", el)

            let away_ft = null
            if (await hasElement("./div/div/div//div[@data-testid='right_score']/span[contains(@class, 'currentScore')]", el, 0))
                away_ft = await getText("./div/div/div//div[@data-testid='right_score']/span[contains(@class, 'currentScore')]", el)

            event_cells.push({
                id,
                url,
                date: [date_1, date_2],
                hometeam,
                awayteam,
                home_ft,
                away_ft,
            })
        }
        return event_cells
    }

    async function change_tab_match(tab_name) {
        console.log("-------------------------------------------")
        console.log(">> change_tab_match:")
        console.log("tab_name", tab_name)
        const tab_ids = {
            'Detalhes': 'details',
            'Probabilidades': 'additional_odds',
            'Formações': 'lineups',
            'Estatísticas': 'statistics',
            'Comentário': 'commentary',
            'Classificação': 'standings',
            'Partidas': 'matches',
        }
        if (!tab_ids.hasOwnProperty(tab_name)) throw new Error(`Não foi encontrado a aba: ${tab_name}`)
        const base_xpath = "//div[./div/div/span[text()='Partidas']]/div[last()]/div[last()]/div[2]/div/div/div[1]/div/div/div[last()]/div[1]/div/div/div/h2"
        console.log("base_xpath", base_xpath)
        if (!(await hasElements(base_xpath))) throw new Error(`Não foi encontrado os elementos das tabulações`)
        let elements = await getElements(base_xpath)
        console.log("elements", elements)
        let has_found = false
        for (let i = 0; i < elements.length && !has_found; i++) {
            console.log("------------")
            let el = elements[i]
            let data_id = await getAttr(el, 'data-tabid')
            console.log("data_id", data_id)
            if (tab_ids[tab_name] == data_id) {
                let status = await waitChangeStyle(`${base_xpath}[${i+1}]`, 'border-bottom-color', async () => await clickElement('./a', el))
                console.log('status', status)
                has_found = true
            }
        }
        if (!has_found) throw new Error(`Não foi possível clicar na aba: ${tab_name}`)
        return true
    }

    async function select_match(id) {
        console.log("-------------------------------------------")
        console.log(">> select_match:")
        const base_xpath = `//div[@data-panelid='date']/div/div[1]/div/div[last()]//a[@data-id='${id}']`
        let status = await waitChangeStyle(`${base_xpath}/div/div`, 'background-color', async () => await clickElement(base_xpath))
        console.log('status', status)
        return status
    }

    async function get_match_information() {
        let info = {}
        const base_xpath = "//div[./div/div/span[text()='Partidas']]/div[last()]/div[last()]/div[2]/div/div/div[1]/div/div"
        const first_section = `${base_xpath}/div[1]`

        let id = await getAttr(`${base_xpath}/a`, 'data-id')
        let country = await getText(`${first_section}/div[1]//li[1]/a`)
        let name_competition = await getText(`${first_section}/div[1]//li[2]/a`)
        let competition_url = await getAttr(`${first_section}/div[1]//li[2]/a`, 'href')

        // Buscar o placar do jogo
        let home_ft = null
        let away_ft = null
        const hour_and_date_xpath = `${first_section}/div[2]/div[./div[@data-testid='left_team']]/div[not(@data-testid)]/div`
        if ((await hasElement(`${hour_and_date_xpath}/div/div[1]//span[@data-testid='left_score']`, document, 100))) {
            home_ft = await getText(`${hour_and_date_xpath}/div/div[1]//span[@data-testid='left_score']`)
        }
        if ((await hasElement(`${hour_and_date_xpath}/div/div[1]//span[@data-testid='right_score']`, document, 100))) {
            away_ft = await getText(`${hour_and_date_xpath}/div/div[1]//span[@data-testid='right_score']`)
        }

        // Buscar o horario do jogo
        let date = null
        let time = null
        let lines = await getElements(`${first_section}/div[2]/div[not(@data-testid='scorer_list')]`, document, 100)
        if (lines.length == 1) { // Jogo hoje ou futuro
            let line_base_xpath = `${first_section}/div[2]/div[not(@data-testid='scorer_list')]`
            // Jogo de hoje
            if (await hasElement(`${line_base_xpath}/div[not(@data-testid)]/div/span[text()='Hoje' or text()='Amanhã']`, document, 100)) {
                time = await getText(`${line_base_xpath}/div[not(@data-testid)]/div/span[1]`)
                date = await getText(`${line_base_xpath}/div[not(@data-testid)]/div/span[2]`)
            } else { // Jogo futuro
                date = await getText(`${line_base_xpath}/div[not(@data-testid)]/div/span[1]`)
                time = await getText(`${line_base_xpath}/div[not(@data-testid)]/div/span[2]`)
            }
        } else { // Jogo passado
            let line_base_xpath = `(${first_section}/div[2]/div[not(@data-testid='scorer_list')][1])`
            date = await getText(`${line_base_xpath}/div/span[1]`)
            time = await getText(`${line_base_xpath}/div/span[2]`)
        }

        let hometeam_url = await getAttr(`${first_section}/div[last()]//div[@data-testid='left_team']//a`, 'href')
        let hometeam_emblem_url = await getAttr(`${first_section}/div[last()]//div[@data-testid='left_team']//a//img`, 'src')
        let hometeam = await getText(`${first_section}/div[last()]//div[@data-testid='left_team']//a//*[name()='bdi']`)
        
        let awayteam_url = await getAttr(`${first_section}/div[last()]//div[@data-testid='right_team']//a`, 'href')
        let awayteam_emblem_url = await getAttr(`${first_section}/div[last()]//div[@data-testid='right_team']//a//img`, 'src')
        let awayteam = await getText(`${first_section}/div[last()]//div[@data-testid='right_team']//a//*[name()='bdi']`)

        competition_url = `https://www.sofascore.com${competition_url}`
        hometeam_url = `https://www.sofascore.com${hometeam_url}`
        awayteam_url = `https://www.sofascore.com${awayteam_url}`

        info = {
            id,
            date,
            time,
            country,
            name_competition,
            competition_url,
            hometeam,
            hometeam_url,
            hometeam_emblem_url,
            awayteam,
            awayteam_url,
            awayteam_emblem_url,
            home_ft,
            away_ft,
        }

        return info
    }

    async function read_statistics_match() {
        console.log("-------------------------------------------")
        console.log(">> read_statistics_match:")
        const link_xpath = "//div[./div/div/span[text()='Partidas']]/div[last()]/div[last()]/div[2]/div/div/div[1]/div/div[last()]/a"
        const id = await getAttr(link_xpath, 'data-id')
        
        const base_xpath = "//div[./div/div/span[text()='Partidas']]/div[last()]/div[last()]/div[2]/div/div/div[1]/div/div[last()]/div[last()]/div[last()]/div[@data-panelid]/div"

        const read_base_xpath = `${base_xpath}/div[@data-panelid]/div`
        const get_section_xpath = (section_name) => {
            return `${read_base_xpath}/div[./div/div/span[text()='${section_name}']]/div[last()]`
        }
        const get_stats_line_xpath = (section_name, stat_name) => {
            const section_xpath = get_section_xpath(section_name)
            return `${section_xpath}/div/div[./*[name()='bdi'][2]/div//span[text()='${stat_name}']]`
        }
        const get_button_xpath = (button_name) => {
            return `${base_xpath}/div[not(@data-panelid)]//div[@data-tabid and ./*[name()='bdi'][text()='${button_name}']]`
        }
        const click_button = async (button_name) => {
            const xpath = get_button_xpath(button_name)
            let status = await waitChangeStyle(xpath, 'background-color', async () => await clickElement(xpath))
            console.log("Mudou de aba: ", status)
        }

        await change_tab_match('Estatísticas')
        if (!(await hasElement(get_section_xpath('Visão geral da partida')))) throw new Error("Não foi possível carregar a aba de estatísticas")

        let stats = {
            id,
            'ft': {},
            'ht': {},
            '2t': {},
        }

        const reading = async () => {
            
            const read = async (section_name, stat_name, extra_xpath = '') => {
                const get_team_match_xpath = (position) => {
                    return `${get_stats_line_xpath(section_name, stat_name)}/*[name()='bdi'][${position}]/span${extra_xpath}`
                } 
                const home_value_xpath = get_team_match_xpath(1)
                const away_value_xpath = get_team_match_xpath(3)

                let home_value = null
                let away_value = null

                if (await hasElement(home_value_xpath, document, 0)) {
                    home_value = await getText(home_value_xpath)
                }
                if (await hasElement(away_value_xpath, document, 0)) {
                    away_value = await getText(away_value_xpath)
                }

                return {
                    home_value,
                    away_value,
                }
            }

            let struct = {
                ball_possession: {
                    home_value: null,
                    away_value: null,
                },
                expected_goals: {
                    home_value: null,
                    away_value: null,
                },
                big_chances: {
                    home_value: null,
                    away_value: null,
                },
                goalkeeper_saves: {
                    home_value: null,
                    away_value: null,
                },
                corners: {
                    home_value: null,
                    away_value: null,
                },
                faults: {
                    home_value: null,
                    away_value: null,
                },
                passes: {
                    home_value: null,
                    away_value: null,
                },
                disarms: {
                    home_value: null,
                    away_value: null,
                },
                fouls_direct_shots: {
                    home_value: null,
                    away_value: null,
                },
                yellow_cards: {
                    home_value: null,
                    away_value: null,
                },

                // ---------------------------------------------
                // Informações de finalizações
                shots: {
                    home_value: null,
                    away_value: null,
                },
                shots_on_target: {
                    home_value: null,
                    away_value: null,
                },
                shots_hit_woodwork: {
                    home_value: null,
                    away_value: null,
                }, // Chutes na trave
                shots_off_target: {
                    home_value: null,
                    away_value: null,
                },
                shots_saved: {
                    home_value: null,
                    away_value: null,
                },
                shots_inside_box: {
                    home_value: null,
                    away_value: null,
                }, // Chutes dentro da área
                shots_outside_box: {
                    home_value: null,
                    away_value: null,
                }, // Chutes fora da área


                // ---------------------------------------------
                // Informações de Ataque
                big_chances_scored: {
                    home_value: null,
                    away_value: null,
                },
                big_chances_missed: {
                    home_value: null,
                    away_value: null,
                },
                through_pass: {
                    home_value: null,
                    away_value: null,
                }, // Passe em profundidade
                actions_penalty_area: {
                    home_value: null,
                    away_value: null,
                }, // Ações com a bola na área de pênalti
                fouls_drawn_final_third: {
                    home_value: null,
                    away_value: null,
                }, // Faltas sofridas no terço final
                offsides: {
                    home_value: null,
                    away_value: null,
                }, // Impedimentos

                // ---------------------------------------------
                // Informações de Passes
                accurate_passes: {
                    home_value: null,
                    away_value: null,
                }, // Passes certos
                throw_ins: {
                    home_value: null,
                    away_value: null,
                }, // Leterais
                runs_final_third: {
                    home_value: null,
                    away_value: null,
                }, // Entradas no terço final

                // ---------------------------------------------
                // Informações de Duelos
                tackles_lost: {
                    home_value: null,
                    away_value: null,
                }, // Desarmes sofridos

                // ---------------------------------------------
                // Informações de Defesa
                total_tackles: {
                    home_value: null,
                    away_value: null,
                }, // Total de desarme
                interceptions: {
                    home_value: null,
                    away_value: null,
                }, 
                ball_recoveries: {
                    home_value: null,
                    away_value: null,
                },
                clearances: {
                    home_value: null,
                    away_value: null,
                }, // Desarme de jogadas perigosas
            }
            
            // -------------------------------------------------------
            // Visão geral
            struct['ball_possession'] = await read('Visão geral da partida', 'Posse de bola', '/span')
            struct['expected_goals'] = await read('Visão geral da partida', 'Gols esperados (xG)')
            struct['big_chances'] = await read('Visão geral da partida', 'Grandes chances')
            struct['goalkeeper_saves'] = await read('Visão geral da partida', 'Defesas do goleiro')
            struct['corners'] = await read('Visão geral da partida', 'Escanteios')
            struct['faults'] = await read('Visão geral da partida', 'Faltas')
            struct['passes'] = await read('Visão geral da partida', 'Passes')
            struct['disarms'] = await read('Visão geral da partida', 'Desarmes')
            struct['fouls_direct_shots'] = await read('Visão geral da partida', 'Faltas (Tiros Diretos)')
            struct['yellow_cards'] = await read('Visão geral da partida', 'Cartões amarelos')
            
            // ---------------------------------------------
            // Informações de finalizações
            struct['shots'] = await read('Finalizações', 'Finalizações')
            struct['shots_on_target'] = await read('Finalizações', 'Finalizações no gol')
            struct['shots_hit_woodwork'] = await read('Finalizações', 'Finalizações na trave') // Chutes na trave
            struct['shots_off_target'] = await read('Finalizações', 'Finalizações para fora')
            struct['shots_saved'] = await read('Finalizações', 'Chutes defendidos')
            struct['shots_inside_box'] = await read('Finalizações', 'Finalizações de dentro da área') // Chutes dentro da área
            struct['shots_outside_box'] = await read('Finalizações', 'Finalizações de fora da área') // Chutes fora da área
            
            // ---------------------------------------------
            // Informações de Ataque
            struct['big_chances_scored'] = await read('Ataque', 'Grandes chances marcados')
            struct['big_chances_missed'] = await read('Ataque', 'Grandes chances perdidas')
            struct['through_pass'] = await read('Ataque', 'Passe em profundidade') // Passe em profundidade
            struct['actions_penalty_area'] = await read('Ataque', 'Ações com a bola na área de pênalti') // Ações com a bola na área de pênalti
            struct['fouls_drawn_final_third'] = await read('Ataque', 'Faltas sofridas no terço final') // Faltas sofridas no terço final
            struct['offsides'] = await read('Ataque', 'Impedimentos') // Impedimentos

            // ---------------------------------------------
            // Informações de Passes
            struct['accurate_passes'] = await read('Passes', 'Passes certos') // Passes certos
            struct['throw_ins'] = await read('Passes', 'Laterais') // Leterais
            struct['runs_final_third'] = await read('Passes', 'Entradas no terço final') // Entradas no terço final

            // ---------------------------------------------
            // Informações de Duelos
            struct['tackles_lost'] = await read('Duelos', 'Desarmes sofridos') // Desarmes sofridos

            // ---------------------------------------------
            // Informações de Defesa
            struct['total_tackles'] = await read('Defendendo', 'Tackles no total') // Total de desarme
            struct['interceptions'] = await read('Defendendo', 'Interceptações') 
            struct['ball_recoveries'] = await read('Defendendo', 'Recuperações de bola')
            struct['clearances'] = await read('Defendendo', 'clearances') // Desarme de jogadas perigosas

            return struct
        }

        stats['ft'] = await reading()
        await click_button('1º')
        stats['ht'] = await reading()
        await click_button('2º')
        stats['2t'] = await reading()

        return stats
    }
    """

class LeaguePage(BaseView):
    def __init__(self, driver: DriverInterface):
        super().__init__(driver)

    def navigate_league_page(self, url: str, timeout: int = 180):
        from Automation.View.Exceptions.NavigateLeaguePageException import NavigateLeaguePageException
        from Automation.View.Exceptions.TimeoutPageException import TimeoutPageException
        
        self.actions.navigate_url(url)
        check_xpath = f"//main/div/div[1]/div/ul/li[last()]/h1[contains(text(), 'Classificações, jogos, resultados')]"
        if not self.actions.has_element(check_xpath):
            raise NavigateLeaguePageException()
        
        try:
            self.actions.is_page_complete(timeout)
        except TimeoutError:
            raise TimeoutPageException()

        return self;

    def click_per_date(self, ):
        self.actions.click_element("//div[@data-tabid and text()='Por data']")

    def read_event_cells(self, ) -> List[EventCell]:
        SCRIPT = SCRIPT_JS + r"""
            const callback = arguments[arguments.length - 1];

            async function main() {
                try {
                    let response = await get_event_cells()
                    callback(response);
                } catch (e) {
                    error = { error: e.message }
                    callback(error)
                }
            }

            main()
        """

        # input("Esperando ler todos os eventos...")

        all_events = []
        self.driver.get().set_script_timeout(120)
        all_events = self.driver.get().execute_async_script(
            SCRIPT
        )
        print(f"all_events: {all_events}")

        event_cells: List[EventCell] = []
        for event in all_events:
            id = event['id']
            url = event['url']
            hometeam = event['hometeam']
            awayteam = event['awayteam']
            home_ft = event['home_ft']
            away_ft = event['away_ft']
            date = None
            part_1, part_2 = event['date']

            # print(f"-"*30)
            # print(f"id: {id}")
            # print(f"url: {url}")
            # print(f"part_1: {part_1}")
            # print(f"part_2: {part_2}")
            # print(f"hometeam: {hometeam}")
            # print(f"awayteam: {awayteam}")
            # print(f"home_ft: {home_ft}")
            # print(f"away_ft: {away_ft}")
            # input("Verificando...")


            # Criar o datetime para a data
            if part_2 == '-' or re.search(r"^\s*\d{2}\:\d{2}\s*$", part_1):
                date = get_day_midnight(date_now())
            else:
                date = parse_date_with_format(part_1, "<dd>/<mm>/<yy>")
            
            # print(f"id: {id}")
            # print(f"url: {url}")
            # print(f"date: {date}")
            # print(f"hometeam: {hometeam}")
            # print(f"awayteam: {awayteam}")
            # print(f"home_ft: {home_ft}")
            # print(f"away_ft: {away_ft}")
            # input("Verificando...")

            # Montar o objeto
            event = EventCell()
            event.set_all({
                "id": id,
                "url": url,
                "date": date,
                "hometeam": hometeam,
                "awayteam": awayteam,
                "home_ft": home_ft,
                "away_ft": away_ft,
            })

            # Adicionar dentro da lista
            event_cells.append(event)
        
        return event_cells

    def change_tab_in_match(self, tab_name: str):
        SCRIPT = SCRIPT_JS + r"""
            const tab_name = arguments[0];
            const callback = arguments[arguments.length - 1];

            async function main() {
                try {
                    let response = await change_tab_match(tab_name)
                    callback(response);
                } catch (e) {
                    error = { error: e.message }
                    callback(error)
                }
            }

            main()
        """

        input("Esperando para trocar de aba...")

        self.driver.get().set_script_timeout(120)
        status = self.driver.get().execute_async_script(
            SCRIPT,
            tab_name,
        )

        return status

    def select_match(self, event: EventCell):
        SCRIPT = SCRIPT_JS + r"""
            const id = arguments[0];
            const callback = arguments[arguments.length - 1];

            async function main() {
                try {
                    let response = await select_match(id)
                    callback(response);
                } catch (e) {
                    error = { error: e.message }
                    callback(error)
                }
            }

            main()
        """

        # input(f"Esperando selecionar a partida...")

        self.driver.get().set_script_timeout(120)
        status = self.driver.get().execute_async_script(
            SCRIPT,
            event.get('id'),
        )

        return status

    def read_information_match(self, competition: Competition) -> Match:
        SCRIPT = SCRIPT_JS + r"""
            const callback = arguments[arguments.length - 1];

            async function main() {
                try {
                    let response = await get_match_information()
                    callback(response);
                } catch (e) {
                    error = { error: e.message }
                    callback(error)
                }
            }

            main()
        """

        # input(f"Esperando ler a partida...")

        self.driver.get().set_script_timeout(120)
        match_data = self.driver.get().execute_async_script(
            SCRIPT
        )


        if not re.search(r"(\d{2})[\/\-](\d{2})[\/\-](\d{4})", match_data['date']):
            if re.search(r"^\s*hoje\s*$",  match_data['date'], flags=re.I):
                match_data['date'] = get_day_midnight(date_now())
            elif re.search(r"^\s*amanh.\s*$",  match_data['date'], flags=re.I):
                match_data['date'] = get_day_midnight(add_day(date_now()))
            else:
                raise ValueError(f"Não identificado o parse da data: {match_data['date']}")
        else:
            match_data['date'] = parse_date_with_format(match_data['date'], "<dd>/<mm>/<yyyy>")
        
        match_data['time'] = parse_time(match_data['time'])

        print(f"match_data: {match_data}")

        match: Match = Match(
            id = match_data['id'],
            date = match_data['date'],
            time = match_data['time'],
            competition = competition,
            hometeam = match_data['hometeam'],
            hometeam_url = match_data['hometeam_url'],
            hometeam_emblem_url = match_data['hometeam_emblem_url'],
            awayteam = match_data['awayteam'],
            awayteam_url = match_data['awayteam_url'],
            awayteam_emblem_url = match_data['awayteam_emblem_url'],
            home_ft = match_data['home_ft'],
            away_ft = match_data['away_ft']
        )

        return match
    
    def read_statistics_match(self, ) -> List[TimeStatistics]:
        SCRIPT = SCRIPT_JS + r"""
            const callback = arguments[arguments.length - 1];

            async function main() {
                try {
                    let response = await read_statistics_match()
                    callback(response);
                } catch (e) {
                    error = { error: e.message }
                    callback(error)
                }
            }

            main()
        """

        input(f"Esperando ler os stats da partida...")

        self.driver.get().set_script_timeout(120)
        statistics_match = self.driver.get().execute_async_script(
            SCRIPT
        )

        # print(f"statistics_match: {statistics_match}")

        match = []

        match.append(
            HalfTimeStatistics(
                id=statistics_match['id'],
                **statistics_match['ht']
            )
        )

        match.append(
            SecondTimeStatistics(
                id=statistics_match['id'],
                **statistics_match['2t']
            )
        )

        match.append(
            FullTimeStatistics(
                id=statistics_match['id'],
                **statistics_match['ft']
            )
        )


        # for time in ['ft', 'ht', '2t']:
        #     # team = TimeStatistics()
        #     team = TimeStatistics(
        #         id=statistics_match['id'],
        #         time=time,
        #         **statistics_match[time]
        #     )

        #     print("-"*80)
        #     print(team.get_all())

        #     match.append(team)

        return match