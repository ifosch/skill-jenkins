# opsdroid skill Jenkins

A skill to interact with Jenkins.

## Requirements

A Jenkins setup.

## Configuration

You can add this skill to your opsdroid powered bot by adding the following to your `configuration.yaml`:

```
skills:
  ...
  - name: jenkins
    repo: https://github.com/ifosch/skill-jenkins.git
    url: https://yourjenkins.setup
    username: username
    password: $JENKINS_TOKEN
```

Then, use `$JENKINS_TOKEN` environment variable to provide the bot's Jenkins user token securely.

## Usage

#### `list`

Lists the jobs available in Jenkins.
```
user: list
opsdroid: one_job
another_job
...
```

#### `build job-name [param=value [...]]`

Runs `job-name` using the list of params for the job invocation, and responds with a link to the job page.
```
user: build my-job param1=value1
opsdroid: Building job-name with parameters param1=value1 (https://yourjenkins.setup/job/my-job/)
``
