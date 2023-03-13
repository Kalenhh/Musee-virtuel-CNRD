#coding:utf-8


from setuptools import setup

setup(
	name = "musee",
	options = {
		'build_apps':{
			'gui_apps' :{
				'musee': 'main.py'
			}
		}
	}
)