#!/bin/sh

# Configure git
git config --global user.name "semantic-release (via GitlabCI)"
git config --global user.email "tue.gitlab@momotor.org"
git checkout "$CI_COMMIT_REF_NAME"
git status

set -eux

# Bump the version
if [ "$CI_COMMIT_REF_PROTECTED" = "true" ]; then
  semantic-release -v --strict version
  semantic-release -v publish
else
  semantic-release -v version --no-changelog --no-vcs-release
fi
