from setuptools import setup

setup(
    name='musee',
    options={
        'build_apps': {
            'gui_apps': {
                'musee': 'main.py',
            },
            "icons" : {"musee":["images/icone_256.png"]},

        

            'include_patterns': [
                '**/*.png',
                '**/*.txt',
                '**/*.wav'
            ],

            'plugins': [
                'time',
                'os',
            ],

            'platforms': ['win_amd64'],

            'plugins': ['pandagl', 'p3openal_audio'],
        }
    }
)