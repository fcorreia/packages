#!/bin/bash
##
##
##
## Shell parameters documentation
## https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html

## This is a script to automate some build operations when pdsng build tools are giving to
## much work, but in the end, a rpm build MUST be possible with pdsng build tool

## RPMBUILDS
# -bp   Executa o %prep
# -bc   Executa o %prep, %build
# -bi   Executa o %prep, %build, %install, %check
# -bb   Executa o %prep, %build, %install, %check e gera o pacote binário
# -ba   Executa o %prep, %build, %install, %check e gera o pacote binário e o pacote com o código fonte
# -bl   Verifica os ficheiros listados em %files


##
## Possible Snapshot revision
## r1494586391.gb79d383
## git:  "$(git log --format=%ct.g%h)"
##


## rpmbuild root folder structure
RPMTOPDIR=${RPMTOPDIR:-"${HOME}/rpmbuild"}

PKG_RELEASE_NUMBER=1

PKG_RELEASE_NAME=${PKG_RELEASE_NAME:-"skywalker"}

DOCKER_IMAGE_NAME="build/centos:7"
DOCKER_IMAGE_DOCKERFILE="centos7.Dockerfile"
DOCKER_CONTAINER_NAME=${DOCKER_CONTAINER_NAME:-"build-el7"}


function get_real_path {
    LINUX_OS=$(uname | grep Linux)
    MACOSX=$(uname | grep Darwin)
    if [ ${LINUX_OS} ]; then
        echo "$(dirname $(readlink -f $1))"
    elif [ ${MACOSX} ]; then
        echo "import os; print(os.path.abspath(os.path.dirname(\"$1\")))" | python
    else
        echo "Dont know how to deal with OS: $(uname)"
        echo ""
        ##return 1
    fi
}

SCRIPT_LOCATION=$(get_real_path $0)



function init_env(){

    ## the base scturture required for rpmbuild
    echo "Creating base struture @${RPMTOPDIR}"
    mkdir -p ${RPMTOPDIR}/{BUILD,RPMS,SOURCES,SPECS,SRPMS,BUILDROOT}

    RPMBUILD_MACROS=${HOME}/.rpmmacros
    ##
    if [ ! -e ${RPMBUILD_MACROS} ] && [ ! -L ${RPMBUILD_MACROS} ]
    then
        echo "Creating rpmbuild macro file"
        echo "%distnum  %{expand:%%(/usr/lib/rpm/redhat/dist.sh --distnum)}" >> ${RPMBUILD_MACROS}
        echo "%disttype %{expand:%%(/usr/lib/rpm/redhat/dist.sh --disttype)}" >> ${RPMBUILD_MACROS}
        echo "%_defaultdocdir %_prefix/doc" >> ${RPMBUILD_MACROS}
        echo "%_mandir %_prefix/man" >> ${RPMBUILD_MACROS}
    else
        echo "Ignoring rpmbuild macro file, already exists!"
    fi

}


##
## Required information
## RPM_NAME ex: package-name
## RPM_VERSION ex: 1.1.0
## RPM_RELEASE r1494551291.gefb43a6
##
function validate_build(){

    if [ "x${RPM_NAME}" == "x" ]; then
        echo "ERROR: could not determine package name"
        exit 1
    fi


    RPM_SPEC=${RPM_SPEC:-"${RPM_NAME}.spec"}
    if [ ! -e ${RPM_SPEC} ] && [ ! -L ${RPM_SPEC} ]; then
        echo "ERROR: Spec file not found, expected: ${RPM_SPEC}"
        exit 1
    fi

    if [ "x${RPM_VERSION}" == "x"  ]; then

        LINE=( $(egrep   "^[ ]*%define[ ]*version[ ]*([0-9a-zA-Z.]*)" ${RPM_SPEC}) )
        if [ ${#LINE[@]} -gt 2 ]; then
            RPM_VERSION=${LINE[2]}
        fi
        if [ "x${RPM_VERSION}" == "x"  ]; then
            echo "ERROR: could not determine package version"
            exit 1
        fi
    fi


    RPM_ARCHIVE="${RPM_NAME}-${RPM_VERSION}"
    RPM_ARCHIVE_FILE="${RPM_ARCHIVE}-source.tar.gz"

}

##
##  Install build require dependencies
##
function spec_dependencies() {
    validate_build

    yum-builddep ${RPM_SPEC}
}

function submit_spec_rsync(){
    validate_build

    rsync -r --verbose --exclude '.git' --exclude '.git'  "$PWD/" "${RPMTOPDIR}/SOURCES/"
}

function submit_spec(){
    validate_build



    RPM_TMP_DIR=$(mktemp -d)
    RPM_ARCHIVE_DIR="${RPM_TMP_DIR}/${RPM_ARCHIVE}"
    mkdir ${RPM_ARCHIVE_DIR}
    cp -rp .    ${RPM_ARCHIVE_DIR}

    SCM_FOLDER="${RPM_ARCHIVE_DIR}/.svn"
    if [ -e "${SCM_FOLDER}" ]; then
        rm -rf  ${SCM_FOLDER}
    fi
    SCM_FOLDER="${RPM_ARCHIVE_DIR}/.git"
    if [ -e "${SCM_FOLDER}" ]; then
        rm -rf  ${SCM_FOLDER}
    fi
    SCM_FOLDER="${RPM_ARCHIVE_DIR}/.hg"
    if [ -e "${SCM_FOLDER}" ]; then
        rm -rf  ${SCM_FOLDER}
    fi


    rm -rf      ${RPM_ARCHIVE_DIR}/${RPM_ARCHIVE_FILE}

    ## For old svn versions clear all .svn folders
    for i in $(find ${RPM_ARCHIVE_DIR} | grep [.]svn$ )
    do
        rm -rf $i;
    done



    STORE_PWD=$PWD
    cd ${RPM_TMP_DIR}
    tar -czf ${RPM_ARCHIVE_FILE} ${RPM_ARCHIVE}

    mv  "${RPM_ARCHIVE_FILE}" "${RPMTOPDIR}/SOURCES"
    mv  "${RPM_ARCHIVE_DIR}/${RPM_SPEC}" "${RPMTOPDIR}/SPECS"
    cd  ${STORE_PWD}
    rm  -rf ${RPM_TMP_DIR}
}



function build_rpm(){
    validate_build



    ## SNAPSHOT Version
    if [ "x${X_RELEASE_FINAL}" == "x" ]; then

        if [ -z $USER_REV ]; then
            ## only supported after git 2
            USER_REV=$(git log --format=%cd.g%h --date=format:%y%m%d%H%M -n 1)
            ##USER_REV=$(git log --format=%ct.g%h -n 1)
        fi

        export RPM_RELEASE="r${USER_REV}"
    else
        ## Final Release
        if [ -z $USER_REV ]
        then
            export RPM_RELEASE="${PKG_RELEASE_NUMBER}.${PKG_RELEASE_NAME}"
        else
            export RPM_RELEASE="${USER_REV}"
        fi
    fi



    echo "Build package: ${RPM_NAME}, Release: ${RPM_RELEASE}"
    ## --buildroot=${PWD}/rpmbuild
    rpmbuild    --define='%rpm_name  %{expand:   %%(echo ${RPM_NAME})}'  \
                --define='%rpm_version  %{expand:%%(echo ${RPM_VERSION})}'  \
                --define='%rpm_release  %{expand:%%(echo ${RPM_RELEASE} )}'  \
                ${RPM_SPEC} \
                -ba
##	--buildroot=${HOME}/rpmbuild \
}



function rpm_sources {
    validate_build


    spectool    --define "rpm_name ${RPM_VERSION}"  \
                --define "rpm_version ${RPM_VERSION}"  \
                --define "rpm_release ${RPM_RELEASE}"  \
                --get-files --sourcedir  ${RPM_SPEC}
}



function clear_build(){
    validate_build

    echo "Clearing RPM Build Paths: ${RPM_NAME}"

    rm -rf ${RPMTOPDIR}/BUILD/noarch/${RPM_NAME}*
    rm -rf ${RPMTOPDIR}/RPMS/noarch/${RPM_NAME}*
    rm -rf ${RPMTOPDIR}/SOURCES/noarch/${RPM_NAME}*
    rm -rf ${RPMTOPDIR}/SPECS/${RPM_SPEC}
}


function list_build(){
    validate_rpmbuild

    echo "${RPM_NAME}@RPMS"
    list_files $(ls -1 ${RPMTOPDIR}/RPMS/${RPM_NAME}* 2> /dev/null)
    list_files $(ls -1 ${RPMTOPDIR}/RPMS/noarch/${RPM_NAME}* 2> /dev/null)
    list_files $(ls -1 ${RPMTOPDIR}/RPMS/x86_64/${RPM_NAME}* 2> /dev/null)

    echo "${RPM_NAME}@SPECS"
    list_files $(ls -1 ${RPMTOPDIR}/SPECS/${RPM_NAME}* 2> /dev/null)

    echo "${RPM_NAME}@SOURCES"
    list_files $(ls -1 ${RPMTOPDIR}/SOURCES/${RPM_NAME}* 2> /dev/null)

    echo "${RPM_NAME}@BUILD"
    list_files $(ls -1 ${RPMTOPDIR}/BUILD/${RPM_NAME}* 2> /dev/null)

}

function list_files(){

    TOTAL_FILES=0



    if [ ! -z $1 ]
    then
        TF_LIST="${1}"
        for FB in "${TF_LIST[@]}"
        do
            FB=$(basename $FB)
            echo "   $FB"
            TOTAL_FILES=$(( TOTAL_FILES + 1 ))
        done
    fi
    echo "Total: ${TOTAL_FILES}"
}








function container_run_first_time(){
    docker run  \
           --name ${DOCKER_CONTAINER_NAME}  -it \
           -v $HOME/Workspace:/workspace \
           --hostname ${DOCKER_CONTAINER_NAME} \
           ${DOCKER_IMAGE_NAME} /usr/bin/bash
}

function container_start_el7(){
    set +e
    DOCKER_CONTAINER_UUID=( $(docker ps -a | grep ${DOCKER_CONTAINER_NAME}) )

    if [ -z  ${DOCKER_CONTAINER_UUID} ]; then
        echo "Running for the very first time.... like a virgin execution..."
        container_run_first_time
        return
    fi

    if [ "x" == "${DOCKER_CONTAINER_START_FRESH}x" ]; then
        echo "Using Container: ${DOCKER_CONTAINER_UUID}"
        docker start -ai ${DOCKER_CONTAINER_UUID}
    else
        echo "Clearing exisitng container: ${DOCKER_CONTAINER_NAME}[${DOCKER_CONTAINER_UUID}]"
        docker rm ${DOCKER_CONTAINER_UUID}
        ## Clear
        unset DOCKER_CONTAINER_UUID
        echo "Starting a new..."
        container_run_first_time
    fi
}


function container_build(){
  set +e
  if [ -e "${SCRIPT_LOCATION}/../Dockerfile/${DOCKER_IMAGE_DOCKERFILE}" ]; then

      if [ ! -e "${SCRIPT_LOCATION}/../Dockerfile/tmp" ];then
          mkdir -vp "${SCRIPT_LOCATION}/../Dockerfile/tmp";
      fi

      cp -v "${SCRIPT_LOCATION}/rpm-build.sh" \
            "${SCRIPT_LOCATION}/../Dockerfile/tmp/rpm-build.sh"
      docker build -t ${DOCKER_IMAGE_NAME} -f ${SCRIPT_LOCATION}/../Dockerfile/${DOCKER_IMAGE_DOCKERFILE} \
      ${SCRIPT_LOCATION}/../Dockerfile

      rm -rvf "${SCRIPT_LOCATION}/../Dockerfile/tmp"
  else
      echo "Dockerfile not found: ${SCRIPT_LOCATION}/../Dockerfile/${DOCKER_IMAGE_DOCKERFILE}"
  fi
}


function show_help(){
    echo "Usage: rpmbuild.sh [Options]"
    echo "   "
    echo "   --init         Inits the basic structure for building rpms on the user home"
    echo "   --submit       Creates a tarbal with the source and puts it on the rpm build path"
    echo "   --build        Build the rpm on the build path with the name of the current project"
    echo "   --rev [number] Sets the revision number if bulding e beta package"
}


##
## Validates if the value is actually a value
function validate_value {
    if [ "${2:0:1}" == "-" ]; then
        echo "\"$1\" Requires a value";
        exit 1
    fi

    if [ "x$2" == "x" ]; then
        echo "\"$1\" Requires a value";
        exit 1
    fi
}

while [ ! "x" == "x$1" ]; do
    case $1 in
        --init)
            echo "Running Init script"
            X_COMMAND=init_env
        ;;

        --deps)
            X_COMMAND=spec_dependencies
        ;;

        --sources)
            X_COMMAND=rpm_sources
        ;;

        --final)
            X_RELEASE_FINAL="yes"
        ;;

        --repackage)
            validate_value "--repackge" $2
            shift
            PKG_RELEASE_NUMBER=$1
        ;;
        --name)
            shift
            if [ "x" == "x$1" ]; then
              echo "--name requires a value"
              exit 1
            fi
            export RPM_NAME=$1
        ;;

        --version)
            shift
            if [ "x" == "x$1" ]; then
              echo "--version requires a value"
              exit 1
            fi
            export RPM_VERSION=$1
        ;;

        --rev|-r)
            shift
            if [ -z $1 ]; then
                echo "[ERROR] must provid a number when using --rev option"
                exit 1
            fi
            export USER_REV=$1
        ;;

        --file|-f)
            validate_value "--file" $2
            shift
            SPEC_FILE=$(basename $1)
            if [ -e ${SPEC_FILE} ]; then
                export RPM_NAME=${SPEC_FILE%%.*}
            else
                echo "File not found, must be on the same folder as the spec file"
                exit 1
            fi
        ;;
        --submit)
            X_COMMAND=submit_spec_rsync
        ;;

        --build)
            X_COMMAND=build_rpm
        ;;

        --clean)
            X_COMMAND=clear_build
        ;;

        --list|-l)
            X_COMMAND=list_rpmbuild
        ;;

        ## Container  Operations
        --fresh-start)
            DOCKER_CONTAINER_START_FRESH="yes"
            X_COMMAND=container_start_el7
        ;;

        --build-container)
            X_COMMAND=container_build
        ;;

        --start)
            X_COMMAND=container_start_el7
        ;;

        --help|-h)
            X_COMMAND=show_help
            exit 0
        ;;


        *)
            show_help
            exit 0
        ;;
    esac

    ## go to next
    shift
done

if [ "x" == "x$X_COMMAND" ]; then
    echo "No command provided"
    exit 1
fi

set +e
$X_COMMAND
