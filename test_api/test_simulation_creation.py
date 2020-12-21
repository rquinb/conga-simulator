import pytest
import requests

class TestGameSimulation:
    SIMULATIONS_BASE_PATH = "http://server:5000/games-simulations"
    TASK_STATUS_BASE_PATH = f"{SIMULATIONS_BASE_PATH}/task"
    SIMULATION_SUCCESS_STATUS = "SUCCESS"
    SIMULATION_FAILED_STATUS = "FAILURE"
    BASE_REQUEST_BODY = {
                    "numberOfGames": 20,
                    "player1": {
                        "name": "Test player 1",
                        "agentType": "conservative_chooser",
                        "acceptedCardsRange": [1, 12],
                        "maxRestBeforeCutting": 10
                    },
                    "player2": {
                        "name": "Test player 2",
                        "agentType": "conservative_chooser",
                        "acceptedCardsRange": [1, 10],
                        "maxRestBeforeCutting": 8
                    }
            }

    @pytest.fixture(autouse=True)
    def set_up_tear_down_tests(self):
        yield
        requests.delete(f"{self.SIMULATIONS_BASE_PATH}/{self.resource_id}")

    def test_game_simulation_execution_workflow(self):
        response = requests.post(self.SIMULATIONS_BASE_PATH, json=self.BASE_REQUEST_BODY)
        path_to_task_status = response.headers['Location']
        self.resource_id = None
        while True:
            task_status_response = requests.get(path_to_task_status).json()
            self.resource_id = task_status_response['resource_id']
            if task_status_response['state'] == self.SIMULATION_SUCCESS_STATUS or task_status_response['state'] == self.SIMULATION_FAILED_STATUS:
                break
        simulations_response = requests.get(f"{self.SIMULATIONS_BASE_PATH}/{self.resource_id}")
        simulations_results = simulations_response.json()
        assert simulations_response.status_code == 200
        assert simulations_results.get('simulation_id', None) == self.resource_id
        assert simulations_results.get('total_games', None) == self.BASE_REQUEST_BODY['numberOfGames']
        assert simulations_results.get('details', None) is not None
        assert simulations_results.get('created', None) is not None
        assert type(simulations_results.get('mean_rounds_per_game', None)) == float


