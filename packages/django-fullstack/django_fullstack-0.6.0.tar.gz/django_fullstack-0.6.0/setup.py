# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_fullstack',
 'django_fullstack.core',
 'django_fullstack.core.handlers',
 'django_fullstack.core.management',
 'django_fullstack.core.management.commands',
 'django_fullstack.django_vite',
 'django_fullstack.django_vite.core',
 'django_fullstack.django_vite.templatetags',
 'django_fullstack.inertia',
 'django_fullstack.inertia.tests',
 'django_fullstack.inertia.tests.testapp',
 'django_fullstack.scripts',
 'django_fullstack.templatetags']

package_data = \
{'': ['*'],
 'django_fullstack': ['static/dist/*',
                      'templates/react/*',
                      'templates/react/src/*',
                      'templates/react/src/Layout/*',
                      'templates/react/src/assets/*',
                      'templates/react/src/pages/*',
                      'templates/react_typescript/*',
                      'templates/react_typescript/public/*',
                      'templates/react_typescript/src/*',
                      'templates/react_typescript/src/Layout/*',
                      'templates/react_typescript/src/assets/*',
                      'templates/react_typescript/src/pages/*',
                      'templates/vue/*',
                      'templates/vue/src/*',
                      'templates/vue/src/assets/*',
                      'templates/vue/src/components/*',
                      'templates/vue/src/pages/*',
                      'templates/vue/src/public/*',
                      'templates/vue_typescript/*',
                      'templates/vue_typescript/src/*',
                      'templates/vue_typescript/src/assets/*',
                      'templates/vue_typescript/src/components/*',
                      'templates/vue_typescript/src/pages/*',
                      'templates/vue_typescript/src/public/*'],
 'django_fullstack.inertia': ['templates/*']}

install_requires = \
['Django>=3.0,<6.0', 'requests>=2.28.2,<2.40.0']

entry_points = \
{'console_scripts': ['django-fullstack = '
                     'django_fullstack.scripts.django_fullstack:run']}

setup_kwargs = {
    'name': 'django-fullstack',
    'version': '0.6.0',
    'description': "make your project frontend + django with django-fullstack, it's so easy",
    'long_description': '# django-fullstack\n\n#### INTRODUCTION PROJECT\nWe have several projects that use a django-fullstack, which is very impressive and makes it easy for us to connect the frontend and backend. Next, we want to make our django-fullstack usable by many other frontend frameworks or create one that can be chosen among them. We are also continuously developing all our projects well and consistently asking our team to look for any flaws in our django-fullstack.\n\n\n- **Flexsibel** : flexsibel to coding and easy \n- **easy to build** : easy to build frontend & backend\n- **support django 5.0** : support django 5.0 and async django\n- **django friendly** : you can integration django and frontend\n- **Fast To code** : simple code and create new project fast\n\n### requirement\n- python >= 3.9 < 3.13\n- django >= 3.0 < 6.0\n- django-fullstack >= 0.1.0 < 2.0.0\n\n### documentation\n- [introduction](#introduction-project)\n  - [installation](#how-to-install-django-fullstack)\n  - [create project](#how-to-create-project-django-fullstack)\n  - [setup django-fullstack](#setup-to-settingpy)\n  - [create frontend](#make-your-app-react-or-vue)\n  - [install frontend](#install-frontend)\n  - [run server](#run-you-server)\n  - [staticfiles](#staticfiles)\n  - [project to production](#production-your-project)\n- [THANKS FOR SUPPORT](#thanks-you-for-support)\n\n### how to install django-fullstack\n-------------------------------\n**1. install using pip**\n```\npip install django-fullstack\n```\n**or install using poetry**\n```\npoetry add django-fullstack\n```\n\nhow to create project django-fullstack\n-------------------------------------\ncommand using django-fullstack\n```bash\ndjango-fullstack startproject name-project\n```\ncommand using django\n```bash\ndjango-admin startproject name-project\n```\n\nsetup to setting.py\n------------------\n\nAdd to ```setting.py``` on your project\n```python\nINSTALLED_APPS = [\n    ...\'\n    \'django_fullstack\',\n]\n```\n\n```python\n # For Setting Django Fullstack\n    DJANGO_FULLSTACK = {\n        "RENDER": {\n            "INDEX": "index.html",\n            "URL_SSR": "http://localhost:13714",\n            "ENABLED_SSR": False,\n        },\n        "TEMPLATE": {\n            "SERVER_PROTOCOL": "http",\n            "DEV_SERVER_HOST": "localhost",\n            "DEV_SERVER_PORT": 5173,\n            "WS_CLIENT_URL": "@vite/client",\n            "ASSETS_PATH": "static/dist",\n            "STATIC_URL_PREFIX": "", # add if you prefix your url stactic\n        },\n        "STATIC_ROOT": "static",\n        "CSRF_HEADER_NAME": "HTTP_X_XSRF_TOKEN",\n        "CSRF_COOKIE_NAME": "XSRF-TOKEN",\n    }\n```\n\nmake your app react or vue\n--------------------------\ngenerate your file react or vue\n\n```bash\ndjango-fullstack create-app vue #use --typescript for using typescript\n```\n\n```bash\ndjango-fullstack create-app react #use --typescript for using typescript\n```\n\n### Install frontend\nthis command to install package frontend\nsupport ```nodejs v16 - v20``` and ```npm > v9```\n\n```bash \nnpm install \n#or \nyarn install\n#or\npnpm install\n```\n\nrun you server\n----------\n\nTo run the backend and frontend simultaneously, you need to run both by opening two terminals, one for Django and the other for the frontend. Once they are running, you can open your browser using http://localhost:8000 or http://127.0.0.1:8000.\n*1. using python*\n```\npython manage.py runserver\n```\n\n*or using pypy3*\n```python\npypy3 -m manage.py runserver\n```\n\n*run frontend*\n```\nnpm run dev\n```\n**visit your host django http://localhost:8000 or http://127.0.0.1:8000**\n\nstaticfiles\n------------\nif you want to display image or other file in a non-conventional way react and vue, the use folowing :\n\n**Image and other file**\n```html\n<img className="w-full lg:w-[60%]" src="/static/image/image.jpg" alt="bla bla"\n    />\n```\nProduction your project\n----------------------\n1. build your frontend\n```bash\nnpm run build\n#or\nyarn run build\n#or\npnpm run build\n```\n2. debug your django in ```setting.py```\n```python\nDEBUG = False\n```\n3. make your project to collectstatic\n```bash\npython manage.py collectstaic\n#or\npypy -m manage.py collectstatic\n```\n\n### thanks you for support\n---------------------\n- *<a href="https://narmadaweb.com">NARMADAWEB</a>*\n- *<a href="https://itec.sch.id"> ITEC </a>*\n- *DJANGO INDONESIA & TEAM*\n',
    'author': 'Raja Sunrise',
    'author_email': 'rajasunsrise@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rajasunrise/django-fullstack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
