# use the config to unit test the files

import sys
import os
import json
import yaml
import inspect
import importlib
from collections import namedtuple


class TestConfig:

    def __init__(self, filename):
        if filename:
            c = self.open_config_file(filename)
            if c:
                self.tests = c.tests

    def open_config_file(self, filename):
        print(f'opening {filename}')
        c = None
        if '.yml' in filename:
            c = self.open_yml(filename)
        elif 'json' in filename:
            c = self.open_json(filename)
        return c

    def open_yml(self, filename):
        with open(filename) as fp:
            c = yaml.load(fp)
        return c

    def open_json(self, filename):
        with open(filename) as fp:
            c = self.json2obj(fp.read())
        return c

    def _json_object_hook(self, d):
        return namedtuple('X', d.keys())(*d.values())

    def json2obj(self, data):
        return json.loads(data, object_hook=self._json_object_hook)


class TestR:

    def __init__(self, config_path):
        self.test_config = TestConfig(config_path)

    def run(self):
        if self.test_config:
            return self.perform_tests(self.test_config.tests)
        else:
            print("ERROR LOADING TEST CONFIG!")

    def get_files(self):
        flz = []
        # get all py files except self
        target_ext = '.py'
        for root, folder, files in os.walk(os.getcwd()):
            flz.extend([f for f in files if f.endswith(target_ext) and os.path.basename(__file__) not in f])
        print(f'found {len(flz)} valid files to import: {flz}')
        return flz


    def perform_tests(self, tests):
        results = []
        mod_funcs = {}
        files = self.get_files()
        # get files in dir
        for f in files:
            effing_name = f.split('.')[0]
            print(f"effing name: {effing_name}")
            try:
                mod = importlib.import_module(effing_name)
                # print(mod)
                all_functions = inspect.getmembers(mod, inspect.isfunction)
                # print(all_functions)
                for af in all_functions:
                    mod_funcs[af[0]] = af[1]
            except ModuleNotFoundError as ex:
                print(ex)

        print(mod_funcs)

        if mod_funcs:
            for t in tests:
                for exp in t.conditions.expected:
                    if isinstance(exp.args, list):
                        t_result = mod_funcs[t.method](*exp.args)
                    elif isinstance(exp.args, dict):
                        t_result = mod_funcs[t.method](**exp.args)
                    else:
                        t_result = mod_funcs[t.method](exp.args)
                    print(f'testing: {t.method} by passing it: {exp.args} -- got: {t_result} | expected: {exp.assertion}')
                    try:
                        assert t_result == exp.assertion, "Fail..."
                        results.append({"pass": True, "id": t.id})
                    except AssertionError as err:
                        print(err)
                        results.append({"pass": False, "id": t.id})
            return results


def process_results(results):
    if results:
        for res in results:
            print(f'{res["id"]} passed: {res["pass"]}')


def main():
    # open config
    print("opening config")
    testr = TestR(os.path.join('./', 'test_config.json'))
    results = testr.run()
    process_results(results)


if __name__ == "__main__":
    main()
