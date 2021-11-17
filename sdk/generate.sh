#!/bin/bash
OPENAPI_GENERATOR_PATH=$(pwd)'/openapi-generator-cli-5.2.1.jar'
YQ_PATH=$(pwd)'/yq_linux_amd64'
GIT_PUSH_PATH=$(pwd)'/git_push.sh'
TMP_FOLDER=$(pwd)'/tmp'

while getopts i:p: flag
do
    case "${flag}" in
        i) INPUT_YML=${OPTARG};;
        p) PROJECT_NAME=${OPTARG};;
    esac
done
PACKAGE_NAME=$(echo $PROJECT_NAME | tr '-' '_')  # Replace dash from project to build package name

echo "######## Generate SDK ########";
echo "Generator Path: $OPENAPI_GENERATOR_PATH";
echo "Input YAML: $INPUT_YML";
echo "Project name: $PROJECT_NAME";
echo "Nom Package: $PACKAGE_NAME";

# Get schema.yml - remove file if exist
if [ -e $TMP_FOLDER/schema.yml ]; then
	rm $TMP_FOLDER/schema.yml
fi
curl $INPUT_YML --output $TMP_FOLDER/schema.yml

# Parse schema version
SCHEMA_VERSION=$($YQ_PATH e '.info.version' $TMP_FOLDER/schema.yml)
echo "Schema version: $SCHEMA_VERSION";

# Check if project folder exist - remove if exist
if [ -d "$TMP_FOLDER/$PROJECT_NAME" ]; then
    rm -rf $TMP_FOLDER/$PROJECT_NAME
fi

# Run OpenAPI generation
java -jar $OPENAPI_GENERATOR_PATH generate -i $TMP_FOLDER/schema.yml -g python --additional-properties packageName=$PACKAGE_NAME,packageVersion=$SCHEMA_VERSION,projectName=$PROJECT_NAME -o $TMP_FOLDER/$PROJECT_NAME

# Push to remote repository
$GIT_PUSH_PATH -i ${TMP_FOLDER}/${PROJECT_NAME} -v ${SCHEMA_VERSION} -r ${PROJECT_NAME}