#!/usr/bin/bash

# Directory that has the clone sitting on the branch gh-pages
OUTPUT_REPO_DIR=${HOME}/src/cb-pages

# Build directory to be used - it will be wiped out if it exists
BUILD_DIR=build-web-deploy

WEB_TOP_DIR=src/web

# It is assumed that this is called sitting in the root
# of the source repo.


echo "####################################################################"
echo "Building main repo"
echo "####################################################################"

rm -rf ${BUILD_DIR}

cmake -B ${BUILD_DIR} . && cmake --build ${BUILD_DIR}


if [ ! -e ${BUILD_DIR}/patches.json ]; then
    echo "No patches.json file found. SOmething went wrong in the build"
    exit 20
fi

echo "####################################################################"
echo "Copy patch file"
echo "####################################################################"

cp ${BUILD_DIR}/patches.json ${WEB_TOP_DIR}/src/assets/patches.json


echo "####################################################################"
echo "Building web app"
echo "####################################################################"

( cd ${WEB_TOP_DIR} ;
  rm -rf ${BUILD_DIR};
    ng build --base-href "/PatchCookbook/" --optimization --output-path ${BUILD_DIR};
)

if [ ! -e  ${WEB_TOP_DIR}/${BUILD_DIR}/index.html ]; then
    echo "Can't find the web files. Something went wrong"
    exit 44
fi


echo "####################################################################"
echo "Copy web files"
echo "####################################################################"

( cd ${OUTPUT_REPO_DIR};
    rm -rf assets *
)

( cd ${WEB_TOP_DIR}/${BUILD_DIR};
    cp -r *  ${OUTPUT_REPO_DIR}
)

( cd ${OUTPUT_REPO_DIR} ;
    git add -A
    git status
)

echo "####################################################################"
echo "Check git status above and commit/push if everything looks okay"
echo "####################################################################"


