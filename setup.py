from setuptools import setup, find_packages

setup(
    name="api--appointment",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.11",
    install_requires=[
        "annotated-types==0.7.0",
        "blinker==1.8.2",
        "certifi==2024.8.30",
        "cffi==1.17.1",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "colorama==0.4.6",
        "cryptography==44.0.2",
        "dnspython==2.6.1",
        "email_validator==2.2.0",
        "Flask==3.0.3",
        "Flask-Cors==5.0.0",
        "flask-openapi3==3.1.3",
        "Flask-SQLAlchemy==3.0.4",
        "greenlet==3.0.3",
        "idna==3.8",
        "iniconfig==2.1.0",
        "itsdangerous==2.2.0",
        "Jinja2==3.1.4",
        "MarkupSafe==2.1.5",
        "nose2==0.15.1",
        "packaging==24.2",
        "pluggy==1.5.0",
        "pycparser==2.22",
        "pydantic==2.7.3",
        "pydantic_core==2.18.4",
        "PyMySQL==1.1.1",
        "pytest==8.3.5",
        "python-dotenv==1.0.1",
        "requests==2.32.3",
        "SQLAlchemy==2.0.34",
        "SQLAlchemy-Utils==0.41.2",
        "typing_extensions==4.6.1",
        "tzdata==2024.1",
        "urllib3==2.2.2",
        "Werkzeug==3.0.4",
    ],
)
