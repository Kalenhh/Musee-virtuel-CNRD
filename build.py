from setuptools import setup

setup(
    name='musee',
    options={
        'build_apps': {
            'gui_apps': {
                'musee': 'main.py',
            },
            "icons" : {"musee":["images/croix.jpg"]},

        

            'include_patterns': [
                '**/*.png',
                '**/*.txt',
                '**/*.wav',
                '**/*.ttf'
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