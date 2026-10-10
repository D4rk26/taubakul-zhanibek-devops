pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        STUDENT_NAME = 'Zhanibek'
        STUDENT_SURNAME = 'Taubakul'
        STUDENT_GROUP = 'IT2-2302'
        STUDENT_ID = '37650'
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
                script {
                    env.GIT_SHA = sh(
                        label: 'Resolve checked-out commit',
                        returnStdout: true,
                        script: 'git rev-parse HEAD'
                    ).trim()
                    env.GIT_SHORT = env.GIT_SHA.take(12)
                    env.CI_IMAGE = "taubakul-zhanibek-devops:jenkins-${env.BUILD_NUMBER}-${env.GIT_SHORT}"
                    env.CI_CONTAINER = "taubakul-zhanibek-ci-${env.BUILD_NUMBER}"
                }
                sh label: 'Verify SCM checkout', script: '''
                    set -eu
                    expected_remote='git@github.com:D4rk26/taubakul-zhanibek-devops.git'
                    actual_remote=$(git config --get remote.origin.url)
                    test "$actual_remote" = "$expected_remote"
                    test -f Jenkinsfile
                    test -f Dockerfile
                    test -f app/server.py
                    test -f tests/test_server.py
                    printf 'Repository: %s\n' "$actual_remote"
                    printf 'Git commit used by Jenkins: %s\n' "$GIT_SHA"
                    printf 'CI image: %s\n' "$CI_IMAGE"
                    printf 'CI container: %s\n' "$CI_CONTAINER"
                '''
            }
        }

        stage('Build') {
            steps {
                sh label: 'Validate project build inputs', script: '''
                    set -eu
                    python3 - <<'PY'
from pathlib import Path

for source in (Path('app/server.py'), Path('tests/test_server.py')):
    compile(source.read_text(encoding='utf-8'), str(source), 'exec')
    print(f'Syntax valid: {source}')
PY
                    bash -n scripts/Taubakul_Zhanibek_system.sh
                    bash -n scripts/generate_application_log.sh
                    docker compose config --quiet
                    grep -Fx 'Name: Zhanibek' Taubakul_Zhanibek_info.txt
                    grep -Fx 'Surname: Taubakul' Taubakul_Zhanibek_info.txt
                    grep -Fx 'Group: IT2-2302' Taubakul_Zhanibek_info.txt
                    grep -Fx 'Student ID: 37650' Taubakul_Zhanibek_info.txt
                    printf 'Build validation completed for %s %s (%s, %s)\n' \
                        "$STUDENT_NAME" "$STUDENT_SURNAME" "$STUDENT_GROUP" "$STUDENT_ID"
                '''
            }
        }

        stage('Test') {
            steps {
                sh label: 'Run application unit tests', script: '''
                    set -eu
                    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
                    printf 'Student: %s %s\n' "$STUDENT_NAME" "$STUDENT_SURNAME"
                    printf 'Group: %s\n' "$STUDENT_GROUP"
                    printf 'Student ID: %s\n' "$STUDENT_ID"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh label: 'Build and inspect CI image', script: '''
                    set -eu
                    docker version --format 'Docker client={{.Client.Version}}/{{.Client.Arch}} server={{.Server.Version}}/{{.Server.Arch}}'
                    printf 'Docker context: %s\n' "$(docker context show)"
                    docker build \
                        --label "org.opencontainers.image.revision=$GIT_SHA" \
                        --label "edu.student.id=$STUDENT_ID" \
                        --tag "$CI_IMAGE" \
                        .
                    test "$(docker image inspect "$CI_IMAGE" --format '{{.Architecture}}')" = 'arm64'
                    test "$(docker image inspect "$CI_IMAGE" --format '{{.Config.User}}')" = '10001:10001'
                    test "$(docker image inspect "$CI_IMAGE" --format '{{index .Config.Labels "org.opencontainers.image.revision"}}')" = "$GIT_SHA"
                    docker image inspect "$CI_IMAGE" \
                        --format 'Image={{.RepoTags}} ID={{.Id}} OS={{.Os}} Arch={{.Architecture}} User={{.Config.User}} Revision={{index .Config.Labels "org.opencontainers.image.revision"}}'
                '''
            }
        }

        stage('Docker Run') {
            steps {
                sh label: 'Run and verify CI container', script: '''
                    set -eu
                    if docker container inspect "$CI_CONTAINER" >/dev/null 2>&1; then
                        docker container stop --time 5 "$CI_CONTAINER" >/dev/null
                        docker container rm "$CI_CONTAINER" >/dev/null
                    fi

                    container_id=$(docker run --detach \
                        --name "$CI_CONTAINER" \
                        --init \
                        --read-only \
                        --cap-drop ALL \
                        --security-opt no-new-privileges:true \
                        --env "STUDENT_NAME=$STUDENT_NAME" \
                        --env "STUDENT_SURNAME=$STUDENT_SURNAME" \
                        --env "STUDENT_GROUP=$STUDENT_GROUP" \
                        --env "STUDENT_ID=$STUDENT_ID" \
                        --label "ci.jenkins.build=$BUILD_NUMBER" \
                        --label "org.opencontainers.image.revision=$GIT_SHA" \
                        "$CI_IMAGE")

                    printf 'Container ID: %s\n' "$container_id"
                    healthy='false'
                    attempt=1
                    while [ "$attempt" -le 30 ]; do
                        health=$(docker container inspect "$CI_CONTAINER" --format '{{.State.Health.Status}}')
                        printf 'Health attempt %s: %s\n' "$attempt" "$health"
                        if [ "$health" = 'healthy' ]; then
                            healthy='true'
                            break
                        fi
                        if [ "$health" = 'unhealthy' ]; then
                            docker container logs "$CI_CONTAINER"
                            exit 1
                        fi
                        attempt=$((attempt + 1))
                        sleep 1
                    done
                    test "$healthy" = 'true'

                    docker exec "$CI_CONTAINER" python3 -c "import urllib.request; body=urllib.request.urlopen('http://127.0.0.1:8080/', timeout=3).read().decode(); assert 'Name: Zhanibek' in body; assert 'Surname: Taubakul' in body; assert 'Group: IT2-2302' in body; assert 'Student ID: 37650' in body; print(body, end='')"
                    docker exec "$CI_CONTAINER" python3 -c "import urllib.request; assert urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3).read() == b'OK\\n'; print('Health endpoint: OK')"
                    docker exec "$CI_CONTAINER" python3 -c "import urllib.error, urllib.request;\ntry:\n urllib.request.urlopen('http://127.0.0.1:8080/not-found', timeout=3)\n raise SystemExit('Expected HTTP 404')\nexcept urllib.error.HTTPError as error:\n assert error.code == 404\n print('Negative endpoint: HTTP 404')"

                    test "$(docker container inspect "$CI_CONTAINER" --format '{{.State.Running}}')" = 'true'
                    test "$(docker container inspect "$CI_CONTAINER" --format '{{.State.Health.Status}}')" = 'healthy'
                    test "$(docker container inspect "$CI_CONTAINER" --format '{{.Config.User}}')" = '10001:10001'
                    test "$(docker container inspect "$CI_CONTAINER" --format '{{.HostConfig.ReadonlyRootfs}}')" = 'true'
                    test "$(docker container inspect "$CI_CONTAINER" --format '{{index .Config.Labels "org.opencontainers.image.revision"}}')" = "$GIT_SHA"

                    docker ps --filter "name=^/${CI_CONTAINER}$" \
                        --format 'Container={{.Names}} Image={{.Image}} Status={{.Status}} Ports={{.Ports}}'
                    docker container inspect "$CI_CONTAINER" \
                        --format 'Container={{.Name}} ID={{.Id}} Running={{.State.Running}} Health={{.State.Health.Status}} User={{.Config.User}} ReadOnly={{.HostConfig.ReadonlyRootfs}} Revision={{index .Config.Labels "org.opencontainers.image.revision"}}'
                    docker container logs "$CI_CONTAINER"
                '''
            }
        }
    }

    post {
        always {
            sh label: 'Remove exact CI container', script: '''
                set -eu
                if [ -n "${CI_CONTAINER:-}" ] && docker container inspect "$CI_CONTAINER" >/dev/null 2>&1; then
                    docker container stop --time 5 "$CI_CONTAINER" >/dev/null
                    docker container rm "$CI_CONTAINER" >/dev/null
                    printf 'Removed CI container: %s\n' "$CI_CONTAINER"
                fi
            '''
        }
    }
}
