# Jenkins CI/CD Pipeline Flask

In this example we see a Flask REST service project that is built using Jenkins.

We use a combination of a CI and a CD pipeline in Jenkins.

## CI Pipeline

The CI pipeline is defined by the `Jenkinsfile-ci` file and contains the 
following stages:

* `unit test`: This stage is where potential unit and component tests (white-box tests) 
    would be executed. These tests run locally and do not require any remote communication.

* `package`: If the tests complete successfully, a wheel file is built from the Python 
    source code, which can then be installed with the `pip` tool.

After a successful build, the wheel file is archived.


## CD Pipeline

The CD pipeline is defined by the `Jenkinsfile-cd` file and contains the 
following stages:

* `download wheel`: The wheel file stored in the Jenkins archive (Artifactory) 
    is downloaded. For this, the Jenkins **copyArtifacts** plugin must be installed.

* `install wheel`: The wheel file, and therefore the application under test, 
    is installed into a virtual environment. 

* `start service`: The Flask server with the REST service is started.
    - `fuser -k ${FLASK_PORT}/tcp || true`: Kill any process currently using that port.
    - `nohup ./${VENV_DIR}/bin/python -m ${FLASK_APP_MODULE} --port=${FLASK_PORT} &`: Start Flask service in background
        - `nohup`: Prevents the process from being killed when the shell exits. 
            Every `sh """..."""` block runs in a temporary shell.
        - `&`: Runs the process in the background, so the pipeline can continue 
    - `sleep 5`: Wait for the service to start

* `acceptance tests`: The full suite of acceptance tests is executed against the running REST service.

In all cases, the Flask server is stopped: `fuser -k ${FLASK_PORT}/tcp || true`


### copyArtifacts Plugin




_Nicoletta Kähling, Egon Teiniker, 2025, GPL v3.0_ 