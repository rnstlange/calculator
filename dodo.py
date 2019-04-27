import yaml


def task_data():
    """Convert data.yaml to data.py"""

    def python_data(targets):
        with open('data.yaml', 'r', encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
            with open(targets[0], 'w', encoding='utf-8') as file:
                file.write('data = ' + str(data) + '\n')

    return {
        'actions': [python_data],
        'file_dep': ['data.yaml'],
        'targets': ['data.py']
    }


def task_gui():
    """Convert gui.ui to gui.py"""

    return {
        'actions': ['pyuic5 gui.ui -o gui.py'],
        'file_dep': ['gui.ui'],
        'targets': ['gui.py']
    }


def task_test():
    """Run main.py"""

    return {
        'actions': ['python main.py']
    }
