import unittest
from unittest.mock import MagicMock
from packages.util.utils.create_status_listener import create_status_listener
from packages.util.tests.__fixtures__.create_status_listener import fixtures

class TestCreateStatusListener(unittest.TestCase):
    def setUp(self):
        self.on_event = MagicMock()

    def tearDown(self):
        self.on_event.reset_mock()

    def test_trigger_events(self):
        for test_case in fixtures["valid"]:
            with self.subTest(test_case_name=test_case["name"]):
                on_event_for_this_subtest = MagicMock()

                operation_enum_from_fixture = test_case.get("operationEnum")
                seed_generation_enum_from_fixture = test_case.get("seedGenerationEnum")

                status_listener_components = create_status_listener({
                    "enums": test_case["enum"],
                    "operationEnums": operation_enum_from_fixture,
                    "seedGenerationEnums": seed_generation_enum_from_fixture,
                    "onEvent": on_event_for_this_subtest,
                })

                on_status_func = status_listener_components["onStatus"]
                force_status_update_func = status_listener_components["forceStatusUpdate"]

                self.assertIsNotNone(on_status_func, "onStatus function should be defined")
                self.assertIsNotNone(force_status_update_func, "forceStatusUpdate function should be defined")

                for status_call_dict in test_case.get("statusCalls", []):
                    on_status_func(status_call_dict)

                for flow_status_value in test_case.get("forceStatusUpdateCalls", []):
                    force_status_update_func(flow_status_value)

                expected_event_calls_from_fixture = test_case.get("eventCalls", [])

                self.assertEqual(
                    on_event_for_this_subtest.call_count,
                    len(expected_event_calls_from_fixture),
                    f"Mock call count mismatch for subtest: {test_case['name']}"
                )

                for i, expected_single_call_args_list in enumerate(expected_event_calls_from_fixture):
                    actual_call_obj = on_event_for_this_subtest.call_args_list[i]
                    actual_args_as_tuple = actual_call_obj.args

                    self.assertEqual(
                        len(actual_args_as_tuple),
                        len(expected_single_call_args_list),
                        f"Argument count mismatch for call {i} in subtest: {test_case['name']}"
                    )
                    self.assertEqual(
                        actual_args_as_tuple[0],
                        expected_single_call_args_list[0],
                        f"Argument value mismatch for call {i}, argument 0 in subtest: {test_case['name']}"
                    )

                    self.assertEqual(
                        actual_call_obj.kwargs,
                        {},
                        f"Keyword arguments were not expected for call {i} in subtest: {test_case['name']}"
                    )

if __name__ == "__main__":
    unittest.main()