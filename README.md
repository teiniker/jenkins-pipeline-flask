# Jenkins CI/CD Pipeline Flask

In this example we see a Flask REST service project that is built, tested
and deployed using Jenkins.

We use a combination of a CI and a CD pipeline in Jenkins:

```
 Flask CI Pipeline (Commit Stage)        Flask CD Pipeline (Acceptance Stage)
+--------------------------------+       +----------------------------------+
| setup                          |       | download wheel  (copyArtifacts)  |
| unit test                      |       | install wheel                    |
| package    -> book_service.whl | ----> | start service                    |
| archive the wheel              |       | acceptance tests                 |
+--------------------------------+       +----------------------------------+
```

The wheel file is the **Release Candidate**. It is built **once** by the
CI pipeline, and the CD pipeline tests exactly this file.


## Project Structure

```
jenkins-pipeline-flask/
├── Jenkinsfile-ci              <-- CI pipeline (Commit Stage)
├── Jenkinsfile-cd              <-- CD pipeline (Acceptance Stage)
├── pyproject.toml              <-- build configuration of the wheel
├── src/book_service/
│   └── book_service.py         <-- Flask REST service
├── tests/
│   ├── unit/                   <-- unit tests (Flask test client)
│   └── acceptance/             <-- acceptance tests (REST API via HTTP)
└── UserStories.md              <-- specification of the acceptance tests
```


## Run the Service Locally

```bash
$ python3 -m venv .venv
$ ./.venv/bin/pip install --editable .
$ ./.venv/bin/book-service --port 9090
```

The command `book-service` is defined in `pyproject.toml`:

```toml
[project.scripts]
book-service = "book_service.book_service:main"
```

When the wheel is installed, pip creates the script `.venv/bin/book-service`,
which calls the function `main()` of the installed package.

Run the tests:

```bash
# Unit tests: no running server needed
$ ./.venv/bin/python -m unittest discover -s tests/unit -p '*_test.py'

# Acceptance tests: the service must be running
$ ./.venv/bin/pip install requests
$ ./.venv/bin/python -m unittest discover -s tests/acceptance -p '*_test.py'
```


## CI Pipeline

The CI pipeline is defined by the `Jenkinsfile-ci` file and contains the
following stages:

* `setup`: Creates a virtual environment and installs the project
    (`pip install --editable .`) together with its dependencies (Flask).

* `unit test`: Runs the unit tests in `tests/unit`. They use the
    **Flask test client**, which calls the request handlers directly,
    without a running server and without network communication.

* `package`: If the tests complete successfully, a wheel file is built
    from the Python source code, which can then be installed with `pip`.

After a successful build, the wheel file is archived in Jenkins
(`archiveArtifacts`, with `fingerprint: true`).


## CD Pipeline

The CD pipeline is defined by the `Jenkinsfile-cd` file.

It is **triggered by the CI pipeline**:

```groovy
triggers
{
    upstream(upstreamProjects: 'Flask CI Pipeline',
             threshold: hudson.model.Result.SUCCESS)
}
```

Every successful build of `Flask CI Pipeline` starts the CD pipeline.
Jenkins registers this trigger when the CD pipeline runs for the first
time, so we have to start it once manually.

The CD pipeline contains the following stages:

* `download wheel`: The wheel file is copied from the CI pipeline. For
    this, the Jenkins **Copy Artifact** plugin must be installed.
    - `upstream(fallbackToLastSuccessful: true)`: Take the wheel of the
        CI build which **triggered** this pipeline. If we start the
        pipeline manually, take the wheel of the last successful build.
    - `fingerprintArtifacts: true`: Jenkins records which CI build the
        wheel comes from.

* `install wheel`: The wheel file, and therefore the application under
    test, is installed into a **new** virtual environment.

* `start service`: The **installed** service is started:
    - `nohup ./.venv/bin/book-service --port 9090 > service.log 2>&1 &`
        - `nohup`: Prevents the process from being killed when the shell
            exits. Every `sh """..."""` block runs in its own shell.
        - `&`: Runs the process in the background, so the pipeline can
            continue.
        - `> service.log 2>&1`: The output of the service is written
            into a file.
    - `echo $! > service.pid`: Store the process ID of the service.
    - **Readiness check**: Send a request to the service every 0.5 s
        until it answers. If it doesn't answer within 10 seconds, the
        stage fails and prints `service.log`.

* `acceptance tests`: The acceptance tests in `tests/acceptance` are
    executed against the running REST service. `BOOK_SERVICE_URL` tells
    them where to find it.

In all cases (`post { always ... }`), the service is stopped with
`kill $(cat service.pid)`. So we stop exactly the process we started.

Note that the Git checkout of the CD pipeline is only used for the
`Jenkinsfile-cd` and the acceptance tests. The service itself comes from
the wheel.


### Copy Artifact Plugin

The Jenkins Copy Artifact plugin (`copyArtifacts`) allows one job or
pipeline to retrieve build artifacts produced by another job or by
earlier builds.

It is essential in multi-job pipelines, promotion workflows, and
**CI/CD setups**.

The plugin lets our Jenkins job copy files (artifacts) from:
* Another Jenkins job
* A specific build of that job
* The same job but a different build number

These artifacts can be: `.whl` files, `.jar`, `.war`, logs, configuration
files or `zip/tar` archives. It copies them into the current workspace so
we can use them in later steps.

_Example_: Copy artifacts in a declarative pipeline
```groovy
copyArtifacts(
    projectName: 'build-job',
    selector: lastSuccessful(),
    filter: 'dist/*.whl',
    target: 'artifacts'
)
```

* `projectName`: job to copy from
* `selector`: which build to choose
* `filter`: which files to copy
* `target`: where to place them inside the workspace

The plugin offers many **selectors**:
* `lastSuccessful()`: Last build that passed
* `lastCompleted()`: Last completed build, regardless of its result
* `specific('42')`: Explicit build number
* `permalink('lastStableBuild')`: Build referenced by a permalink
* `upstream()`: Build that triggered this job
* `buildParameter('BUILD')`: Build selected by a build parameter


## References

* [Jenkins Copy Artifact](https://plugins.jenkins.io/copyartifact/)
* [Jenkins Pipeline Syntax: Triggers](https://www.jenkins.io/doc/book/pipeline/syntax/#triggers)
* [Python Packaging: Entry Points](https://packaging.python.org/en/latest/specifications/entry-points/)

_Nicoletta Kähling, Egon Teiniker, 2025-2026, GPL v3.0_
