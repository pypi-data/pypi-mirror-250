import functools
import pickle
from typing import Optional


class FunctionGatherer:
    def __init__(self) -> None:
        self.gathered_functions = []

    def __call__(self, function):
        self.gathered_functions.append(function)
        return function


class PrecomputeGatherer:
    def __init__(self, cached: Optional[bytes] = None) -> None:
        if cached:
            self.gathered_results = pickle.loads(cached)
        else:
            self.gathered_results = {}

    def __call__(self, function):
        if function.__name__ not in self.gathered_results:
            function_result = function()
            self.gathered_results[function.__name__] = function_result

        @functools.wraps(function)
        def mock_function():
            return self.gathered_results[function.__name__]

        return mock_function

    def export_results(self) -> bytes:
        return pickle.dumps(self.gathered_results)


predict_function = FunctionGatherer()
precompute_function = PrecomputeGatherer()
