# Serverless Framework AWS Python Lambda/Kinesis

## Usage

### SLS Installation

In a terminal run:

```
asdf plugin add serverless https://github.com/pdemagny/asdf-serverless.git
```
and then
```
asdf install
```

NOTE: make sure you have your AWS credentials properly configured and permissions to create resources in AWS

### Deployment

In order to deploy the example, you need to run the following command:

```
$ serverless deploy
```

After running deploy, you should see output similar to:

```bash
Deploying hd-prj to stage dev (us-east-1)

✔ Service deployed to stack hd-prj-dev (112s)

functions:
  hello: hd-prj-dev-hello (1.5 kB)
```

### Invocation

After successful deployment, you can invoke the deployed function by accessing the URL in api-gateway:

endpoint: GET - https://7x9saiixwa.execute-api.us-east-1.amazonaws.com/

Which should result in response similar to the following:

```json
{
    "statusCode": 200,
    "body": "{\"message\": \"I've received your request and pushed some shit to kinesis!\", \"heartRate\": {\"heartRate\": 79, \"rateType\": \"NORMAL\"},, \"input\": {}}"
}
```

### Bundling dependencies

In case you would like to include third-party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).
