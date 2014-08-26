try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='ica',
    version='0.1',
    description='',
    author='',
    author_email='',
    license='',
    url='',
    keywords='',
    long_description='',
    install_requires=[
        "Pylons>=1.0.1rc1",
        "WebOb==1.2",
        "Jinja2",
        "SimpleJson",
        "Dicttoxml",
        "Redis",
        "python3_ldap",
        "MySQL-python",
        "pysqlite",
        "repoze.who",
        "SQLAlchemy>=0.5",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'ica': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors={'ica': [
            ('**.py', 'python', None),
            #('**.js', 'javascript', None),
            ('templates/**.html', 'jinja2', None),
            ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.paster_command]
    db = ica.lib.cli:RedisDB
    user = ica.lib.cli:UserManage

    [paste.app_factory]
    main = ica.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
