import os

from client import build_scenario_log, list_scenarios, send_logs


def scenario_entries(name: str):
    valid = set(list_scenarios())
    if name == "batch":
        return [build_scenario_log(scenario) for scenario in list_scenarios()]
    if name not in valid:
        available = ", ".join(list_scenarios() + ["batch", "list"])
        raise SystemExit(f"Unknown LOG_TEST_SCENARIO '{name}'. Available: {available}")
    return [build_scenario_log(name)]


if __name__ == "__main__":
    scenario = os.getenv("LOG_TEST_SCENARIO", "auth_error")
    address = os.getenv("LOG_COLLECTOR_ADDRESS", "localhost:50051")

    if scenario == "list":
        print("\n".join(list_scenarios() + ["batch"]))
        raise SystemExit(0)

    print(send_logs(scenario_entries(scenario), address))
