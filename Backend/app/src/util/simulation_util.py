import math

from deprecated.classic import deprecated

from app.models.question_collection import QuestionCollection
from app.models.simulation_fragment import SimulationFragment
from app.models.model_selection import ModelSelection
from app.models.task import Task
from app.models.user_scenario import UserScenario


from history.util.result import get_result_response


def find_next_scenario_component(scenario: UserScenario):
    """
    Function to find next component in a scenario by component-index depending on the current counter.
    If no next component can be found, it will return a ResultReponse
    This is probably not a fast way of finding the next component and should be replaced by a better system.
    """
    # todo: find better solution

    # add all components here
    components = [QuestionCollection, SimulationFragment, ModelSelection]
    query = dict(
        index=scenario.state.component_counter,
        template_scenario_id=scenario.template_id,
    )

    for component in components:
        if component.objects.filter(**query).exists():
            # return the next component instance -> gets checked with isinstance() in continue_simulation function
            return component.objects.get(**query)

    # send ResultResponse when scenario is finished

    return get_result_response(scenario)


def end_of_fragment(scenario) -> bool:
    """
    THIS IMPLEMENTATION IS NOT FINAL AND NOT FINISHED (wip for testing)
    This function determines if the end condition of a simulation fragment is reached
    returns: boolean
    """
    # todo philip: clean this up
    try:
        fragment = SimulationFragment.objects.get(
            template_scenario=scenario.template, index=scenario.state.component_counter
        )
    except:
        return False

    if fragment.last:
        return end_of_simulation(scenario)

    tasks_done = Task.objects.filter(user_scenario=scenario, done=True)

    end_types = ["tasks_done", "motivation"]

    for end_type in end_types:
        if fragment.simulation_end.type == end_type:
            if fragment.simulation_end.limit_type == "ge":
                if len(tasks_done) >= fragment.simulation_end.limit:
                    return True
                else:
                    return False


def end_of_simulation(scenario: UserScenario) -> bool:
    tasks = Task.objects.filter(user_scenario=scenario).count()
    tasks_integration = Task.objects.filter(
        user_scenario=scenario,
        unit_tested=True,  # TODO: CAHNGE BACK TO INTEGRATIO TESTED
        # THIS IS ONLY BECAUSE WE CANNOT INTEGRATION TEST YET
    ).count()
    if tasks == tasks_integration:
        return True
    return False


class WorkpackStatus:
    remaining_trainings: int = 0

    meetings_per_day = []

    def __init__(self, days, workpack):
        self.calculate_meetings_per_day(days, workpack)
        self.remaining_trainings = workpack.training

    def calculate_meetings_per_day(self, days, workpack):
        meetings_per_day_without_modulo = math.floor(workpack.meetings / days)
        modulo = workpack.meetings % days
        for day in range(days):
            if day < modulo:
                self.meetings_per_day.append(meetings_per_day_without_modulo + 1)
            else:
                self.meetings_per_day.append(meetings_per_day_without_modulo)

    # def set_remaining_trainings(self, remaining_trainings_today, remaining_work_hours):
    #     if remaining_trainings_today > remaining_work_hours:
    #         self.remaining_trainings = remaining_trainings_today - remaining_work_hours
    #     else:
    #         self.remaining_trainings = 0
